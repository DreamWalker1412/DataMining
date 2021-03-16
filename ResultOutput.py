# ResultOutput


def outputResult(out_file_name, supportDictionary, minConfidence):
    with open(out_file_name, 'w') as f:
        for key in supportDictionary:
            result = []
            if len(key) > 1:
                for item in key:
                    result.append(item)
                print("FrequentSet:" + str(result))
                f.write("FrequentSet:" + str(result) + '\n')
                supportKey = supportDictionary.get(key)
                print("Support: " + str(format(supportKey, '.5f')))
                f.write("Support: " + str(format(supportKey, '.5f')) + '\n')

                for item in result:
                    supportItem = supportDictionary.get(frozenset([item]))
                    confidence = supportKey / supportItem
                    if confidence >= minConfidence:
                        tempList = result.copy()
                        tempList.remove(item)
                        print(str([item]) + '->' + str(tempList), end='  ')
                        print("Confidence: " + str(format(confidence, '.5f')))
                        f.write(str([item]) + '->' + str(tempList) + '  ')
                        f.write("Confidence: " + str(format(confidence, '.5f')) + '\n')
                print('')
                f.write('\n')