
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
from scipy import fftpack

import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# データ ファイルのパス
PATH = 'Q4149CF2.csv'


# In[3]:


# オリジナルの加速度を読み込む。
data = pd.read_csv(PATH, skiprows=6)
data = data.rename(columns={' NS': 'NS'})
print(data.head())


# In[4]:


# オリジナルの加速度の波形を描画する。
fig, (ax_NS, ax_EW, ax_UD) = plt.subplots(ncols=3, figsize=(10,4))

ax_NS.plot(data['NS'])
ax_NS.set_title('NS')

ax_EW.plot(data['EW'])
ax_EW.set_title('EW')

ax_UD.plot(data['UD'])
ax_UD.set_title('UD')


fig.show()


# In[5]:


# 1. データをフーリエ変換する。
fft_df = pd.concat([pd.Series(fftpack.fft(data[column])) for column in data.columns], axis=1)

fft_df = fft_df.rename(columns={0: 'NS', 1: 'EW', 2: 'UD'})
fft_df.head()


# In[6]:


# フィルターをかける。(図3を参照)
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


# In[7]:


# 逆フーリエ変換する。
# 逆フーリエ変換すると、虚部が残る可能性があるので、np.real をかぶせる。
ifft_df = pd.concat([pd.Series(np.real(fftpack.ifft(filtered_df[column]))) for column in filtered_df.columns], axis=1)

ifft_df = ifft_df.rename(columns={0: 'NS', 1: 'EW', 2: 'UD'})
ifft_df.head(14)


# In[23]:


# フィルター処理済みの3成分波形をベクトル的に合成する。


# # 5. a を求める。

# In[204]:


# 6. 計測震度 I を計算する。


# In[190]:


# Iの小数第３位を四捨五入し、小数第２位を切り捨てたものを計測震度として返す。
