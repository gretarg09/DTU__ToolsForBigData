from __future__ import division
from itertools import combinations
import cv2 # for this I needed to install opencv -> pip install opencv-python
import numpy as np
from scipy import spatial
from sklearn.metrics import adjusted_rand_score



######################### FUNCTIONS TO CALCULATE THE DIFFERENCES ###################################
    
# This function takes in a list of key value pairs (image key,  feature vectore) and 
# Finds all combinations of the pairs and then calculated the number of different bits between two hash strings
# It returns a sorted list, sorted in reverse order so the pairs with the highest difference are on the top of the list
def find_cosine_similarity(tuple_pair_array):
    similarities = []

    # find all combinations
    for i in combinations(tuple_pair_array, 2):
                
        similarity =  1 - spatial.distance.cosine(i[0][1], i[1][1])
        similarities.append((i[0],i[1],similarity))

    similarities = sorted(similarities, key =  lambda x:x[2], reverse=False)

    for similarity_pair in similarities:
        output = "{}|{} -  similarity = {}".format(
            similarity_pair[0][0],
            similarity_pair[1][0],
            #similarity_pair[0][1],
            #similarity_pair[1][1],
            similarity_pair[2]
        )

        print output    


######################### RAND INDEX CALCULATIONS ###################################

def rand_index(clusters):
    truth = [
        set(['PC9Q6BW6W8VQ', '4DDXSHKS2IO4', 'VQGCPX8Z6XGH', 'QBH7QIIFQ4UK', 'PJNRJE4KRMVA', 'VU18BXJ7E98V', 'SJM8AQIRRGEM', 'JS2IGMCCE0UR', 'TQ8JXUOLLYM6', 'SHAG7PK12DY3']),
        set(['X0XJZ82P91XP', 'ITCIIVP3NIWT', 'MZQ8UKOI2TH1', 'FWTIVJWGC5W0', '5LBXP3DQB1ZV', 'CFBJKY8U2EJJ', 'AFA0UAQH5R80', 'MTWOUICAOQHH', 'F8875AUQ1YW5', '2OBHSZIX0AMS']),
        set(['HL63F2BNOXQO', 'HHVNVHP7RE44', 'O3EYQ5KCXQN2', '5L48Z43BI5OM', '5MZQ0TJ71OF3', 'MJ3NBDBHKX2Z', 'PT0KESCPZ7UU', '5VAW399EPYMT', 'PKEM4LE0MQ9K', 'LTXMMAQUHLR4']),
        set(['EMEHLAKYA8E6', 'HNL7C8Q3M4HO', '1S4O2POCTDGM', 'DWOZ8DJXK4PO', 'REBYLY0QRKSS', 'MAT24SZ88H1X', '4CU1929MA650', '9220H8P1KB4W', '5D18P9GTGUMD', 'DG1KC6AT1O2S']),
        set(['LC74ZN0KULDF', 'O6DRDN55LGS4', 'WHQZOEVJUI34', '2GEVEDOAWTGZ', 'MM2B45SULBQ4', '5WZSXVXQ2WBN', '0V0CA9OJC2FM', 'WQJ7C35XQ6ZY', '7TYVE8D1TWB4', 'IB45QHV3ZWPN']),
        set(['KVQ0DI7DMA9M', 'N9M13WSJ9O4X', 'ZR48D91D1ZIH', 'X903IBGRY8LF', 'VYS8B8HE6EM1', 'VFZ003C37B5Z', 'MATT3IM1R8K5', 'VI3E9GKO6GPS', 'BCV838KCL850', '5LF9DICID5LS']),
        set(['2H79ACWZUQED', 'ZLIFGZW9D741', '8NUMCA0BWN8W', 'ZPLEWBTAEIXG', '39KDGW6G5QKC', 'M6DX4IDA6OSH', '93CYWYVZIOGZ', 'O90LFFI2ZR1W', 'FG7BBEEDVSYI', 'A6O7JS2Y8CDW']),
        set(['SFR07XTFCCJU', '5EEZNJ918JHG', '0K160AK52ZYS', 'EZUCOY1XGOSO', 'VO8CJU4Z62G8', 'FVMG6J0COUYW', '8CENFQPL2FI5', 'QCBLNBSJUE4X', 'IO7OXN9XLR8B', 'YPPU9HYNYB33']),
        set(['BQI3RYQ1TAJV', 'NOPATUEXOGUV', 'RVX7KINPR50Q', 'LHAT5CZTGWIX', 'HYG0R2DNZQTW', 'LYZ5WFPPDN4C', 'ZH1KIMY7KWYU', 'VWCWOXBEAIRB', 'KD3E9UZFRNFL', 'TSIGN83K0772']),
        set(['P4N2V0NVVV8H', 'YMHF4GAOFNOA', 'EP1H5ZJ5VHLH', 'Z32MBWUK5EAC', '59YXH3WTZEUE', 'H73ZJDYPXHJ9', 'PYMUTU6LGTEK', 'FWR8AQHXYDSQ', 'V3RT1616SU2T', 'HEKXL3LG1FYK']),
        set(['PI64R8RDU5KH', 'S9XAH4MG6NOF', 'WFAZYD4K3BHL', 'AWV4XDBZBNXV', 'U66VLX1FZ4VB', '6P3N8Y3SOUBU', 'QVUKU04SK1IP', 'YCLD5KJBZ9WW', 'GKT85KBXD457', '3ZYOF88E62SK']),
        set(['LDY5SZC34GMH', 'DRQZDUT9I2IX', 'N0RE8W3NKA6F', 'ZQT3SIA3CU7E', '5BERVTCC67NL', 'XBFWVA6VXOUI', '0A3J1A75VD25', '5U99NV1IYXJD', '62RCAEP9V3YQ', 'PDUHWMAFTQUA']),
        set(['VFUYELZ8N98L', 'OPAB10OUZINI', 'PRI2JWRAZRQ2', '7NICDIC6YEJG', 'GI3AS3PL1G6G', 'MZGFXOFYZ3B9', '1GYZIHN8D9YF', '5JV8MT8T7217', '9KQ5PTREJHNG', 'KMSO4053DNKA']),
        set(['94HUNOV6D50Z', '6U4GSNO3HZ9U', 'IYRA8ZQXPCSK', '9M8S1D2ED4X1', '75WSCVHV9RIJ', '8MVEMXM1H0IC', 'OLJRO416ROSQ', 'TYK8MF9HTCSE', '7L2I0KW236DJ', 'GZRUU9MVD5F5']),
        set(['PU2OOPTYI6AF', 'TL2D29GA5YXY', '5OEOC4A11DFL', 'VDYMLFBSRHOD', 'STL4SNVVPH2Q', '9NQROV3KHAFC', 'I9TO1T2YDY0C', 'X3X9FELTJRU9', 'X281EK4DGMWJ', '1BZTVRL7CJPB']),
        set(['PIV7A2LAA2R1', 'N776WD6EU8Q3', '9BVHN720PO3G', 'Q7HYH9EZUFMY', 'VZV2SE7ZOJRJ', 'HGGSF2RGMHYA', 'Y8GUIRV70HB4', 'A9HJ87EGKR8D', 'U58K6OYTTQY4', 'L22AT94NBT0U']),
        set(['OAG1MKHELHFO', 'J2ZXNIG0BPLP', 'GHXX0GDZC2ZJ', 'Q74808QJ9V61', 'KX9V5HTQGPIU', '79KNQAACVXMT', '1T8KUDXSVGTO', 'E2GSJWN0KZ5F', 'QCUIPNF8JE1G', 'JQ9155A40CNK']),
        set(['6M0ITNH532FT', '6OC9OYOTGW3H', 'H7CSJS65M5H4', 'BYC3ODH9BE7M', 'OI2N8AESXCOC', 'F73M1Y00VMQ3', 'XTIDZ33TA21B', '8FW7TDBYR3R6', 'QWM74DETIGU3', 'RAGRTH1HRLWI']),
        set(['VOYHGYGUEI2D', '60FCHT4BLIBE', 'Y834K5B6FDSJ', '4IXLA4JNYZCV', 'SAK6MDHJ0Z56', 'HLAAP1HCYV35', '4Q58ULSTRL2Z', 'GBQBEU144BMT', 'WDBQUVHM7TES', 'IJP10DNTNCNV']),
        set(['V3HS7SDTYQN4', 'E8VCNFOWCW1N', 'RL4MKRP524PU', 'COCSVWTEY6AE', 'WBNMSO7X17PU', 'INRA6NWETUDL', 'RUWUCFQZQH9W', 'GY03QRA6FXCM', '7J1RW84N7IUZ', 'Z86FHQ2O1SVS']),
        set(['LUW4GWH3RP4Z', 'ZZTM0X6OON1U', '1XMN4WYN9ZOG', 'L5SPAW18PX07', '8PBLJBOI3GB1', 'A11Z6M9V9B89', 'GZIGOU721UZZ', '6MUNQE00N2V5', '3OB1UZGIE8ZY', 'E667SMU77M16'])

        ]
    elems = list(set.union(*truth))
    
    # Index of Containing Set
    memory_truth = {}
    memory_clusters = {}
    def ics(element, set_list, set_list_name):
        if set_list_name == "truth":
            if element in memory_truth:
                return memory_truth[element]
        if set_list_name == "clusters":
            if element in memory_clusters:
                return memory_clusters[element]

        for c, s in enumerate(set_list):
            if element in s:
                if set_list_name == "truth":
                    memory_truth[element] = c
                if set_list_name == "clusters":
                    memory_clusters[element] = c
                return c

    x = map(lambda e: ics(e, clusters, 'clusters'), elems)
    y = map(lambda e: ics(e, truth, 'truth'), elems)
   

    return adjusted_rand_score(x,y)





# This function takes in a list of key value pairs (image key, hex value string) and 
# Finds all combinations of the pairs and then calculated the number of different bits between two hash strings
# It returns a sorted list, sorted in reverse order so the pairs with the highest difference are on the top of the list
def find_hamming_distances(tuple_pair_array):
    distances = []

    # find all combinations
    for i in combinations(tuple_pair_array, 2):
        distance =  get_hamming_distance(i[0][1],i[1][1])
        distances.append((i[0],i[1],distance))

    distances = sorted(distances, key =  lambda x:x[2], reverse=True)

    for distance_pair in distances:
        output = "{}|{} - {}|{} - {}".format(
            distance_pair[0][0],
            distance_pair[1][0],
            distance_pair[0][1],
            distance_pair[1][1],
            distance_pair[2]
        )

        print output

# Functions that finds number of different bits between two hash strings  
def get_hamming_distance(hash_string1, hash_string2):
    """Get the number of different bits between two hash strings."""
    dist = 0
    # get diff matrices from hash string
    bits1 = hash_to_bits(hash_string1)
    bits2 = hash_to_bits(hash_string2)

    # compute distance
    for bit1, bit2 in zip(bits1, bits2):
        if bit1 != bit2:
            dist += 1
    return dist

def hash_to_bits(hash_string):
    """Convert a hash string into the corresponding bit string."""
    bits = []
    # Convert into individual hex numbers
    hex_nums = ['0x' + hash_string[i:i+2] for i in range(0, len(hash_string), 2)]
    for hex_num in hex_nums:
        bit_string = bin(int(hex_num, 16))[2:].rjust(8, '0') # binary string
        bits.append(bit_string)
    return "".join(bits) # return as one string
    
    
######################## HASHING ALGORITHMS ##############################

def difference_hash(sum_images,pxls):
    
    img_compared = np.empty((pxls,pxls))
    for i,row in enumerate(sum_images):
        for j,column in enumerate(row):
            if j + 1 == len(row):
                break
            else:
                img_compared[i][j] = row[j] > row[j+1]
    
   # print "The full matrix"
   #print img_compared
    
    hash_string = ""
    for difference in img_compared:
        #print "each line:"
        #print difference 
        decimal_value = 0
        hex_string = []  
        for index, value in enumerate(difference):
            if value: 
                decimal_value += 2**(index % pxls)
            if (index % pxls) == pxls-1:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value  = 0
        hash_string = hash_string +''.join(hex_string) + ' '
    
    return hash_string
    