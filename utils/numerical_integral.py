def numerical_integration(data, index):
    result = [0.0]
    for i in range(1, len(data)):
        result.append((data[i]+data[i-1])*(index[i]-index[i-1]) / 2 + result[i-1])
    return result