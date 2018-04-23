
exec(open("Utils.py").read(), globals())


RANDOM_SEED = 70

############################################################################
data = pd.read_csv('DATA/random_balanced_df_with_Y.csv').dropna()

columns_name = data.columns.get_values()
data.columns = columns_name

energy = []
for string in data.DIRNAME:
    photon = bool(re.findall('MEV', string))
    if photon == True:
        num = re.findall('\d+', string)
        energy.append(int(num[0]))

pd.Series(energy).value_counts()
"""
sns.kdeplot(pd.Series(energy))
plt.xlim(xmin=0)
plt.title( "Density of energy (photons)")
plt.savefig("DATA/Density_enrgy.jpeg")


Y_REG = []
for string in data.DIRNAME:
    photon = bool(re.findall('MEV', string))
    if photon == True:
        num = re.findall('\d+', string)
        Y_REG.append(int(num[0]))
        print string, num[0]

"""
# data['Y'] = Y_REG