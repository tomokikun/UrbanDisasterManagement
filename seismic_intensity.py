# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt


# データ ファイルのパス
PATH = 'Q4149CF2.csv'

# オリジナルの加速度を読み込む。
data = pd.read_csv(PATH, skiprows=6)
data = data.rename(columns={' NS': 'NS'})

# オリジナルの加速度の波形を描画する。
fig, (ax_NS, ax_EW, ax_UD) = plt.subplots(ncols=3, figsize=(10,4))

ax_NS.plot(data['NS'])
ax_NS.set_title('NS')

ax_EW.plot(data['EW'])
ax_EW.set_title('EW')

ax_UD.plot(data['UD'])
ax_UD.set_title('UD')

# fig.show()


# 1. データをフーリエ変換する。
fft_df = pd.concat([pd.Series(fftpack.fft(data[column]))
                    for column in data.columns], axis=1)

fft_df = fft_df.rename(columns={0: 'NS', 1: 'EW', 2: 'UD'})
fft_df.head()


# 2. フィルターをかける。(図3を参照)
def filter_1(f):
    """周期の効果を表すフィルターです。
    """
    return np.sqrt(1 / f)


def filter_high(f):
    """ハイカットフィルターです。
    """
    y = f * 0.1
    result = (1 + 0.694 * y ** 2 + 0.0557 * y ** 6 + 0.009664 * y ** 8
              + 0.00134 * y ** 10 + 0.000155 * y ** 12)
    return 1 / np.sqrt(result)


def filter_low(f):
    """ローカットフィルターです。
    """
    return np.sqrt(1 - np.exp(- (f / 0.5) ** 3))


filtered_df = filter_low(filter_high(filter_1(fft_df)))

filtered_df.head()


# 3. 逆フーリエ変換する。
# 逆フーリエ変換すると、虚部が残る可能性があるので、np.real をかぶせる。
ifft_df = pd.concat([pd.Series(np.real(fftpack.ifft(filtered_df[column]))) for column in filtered_df.columns], axis=1)

ifft_df = ifft_df.rename(columns={0: 'NS', 1: 'EW', 2: 'UD'})
ifft_df.head(14)


# 4. フィルター処理済みの3成分波形をベクトル的に合成する。

def synthesize_vector(x, y, z):
    return np.sqrt(x ** 2 + y ** 2 + z ** 2)


a = []
for row in ifft_df.iterrows():
    a.append(synthesize_vector(row[1]['NS'], row[1]['EW'], row[1]['UD']))

# ベクトル合成の結果
synthesized_series = pd.Series(a)
synthesized_series.head()

# 5. a を求める。


def get_a(syn_data):
    """ベクトル波形(フィルター処理済みの3成分波形をベクトル的に合成したもの)の絶対値がある値 a 以上となる時間の合計を計算したとき、
    これがちょうど 0.3秒となるような a を求めて、その a の値を返します。
    
    具体的には、デジタル記録のサンプリング時間間隔 dt としたとき、 
    ベクトル波形 p を絶対値の大きい順に並べて、 0.3 / dt 番目の値を
    a とする。
    
    サンプリング レートは 100Hz なのでサンプリング間隔は 0.01 sec.
    :param syn_data: 合成済みのデータ
    :type syn_data: pandas.Series
    :return: 条件を満たす a の値
    :rypte: float
    """
    dt = 1 / 100
    max_time = int(0.3 / dt)
    
    syn_data.sort_values(ascending=False)
    return syn_data[max_time]

# 6. Iの小数第３位を四捨五入し、小数第２位を切り捨てたものを計測震度として返す。


from math import floor, log, log2, log10


# I を求めます.
def calc_intensity(tomoki_result):
    cal = lambda x: "{:.2f}".format(round(2 * x + 0.84, 2))
    # log の底が不明なので三種類試します.
    return cal(log(tomoki_result)), cal(log2(tomoki_result)), cal(log10(tomoki_result))


print(f"a: {get_a(synthesized_series)}")
print(f"seismic_intensity: {calc_intensity(get_a(synthesized_series))}")

