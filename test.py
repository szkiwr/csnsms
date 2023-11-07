from block import getLatestBlockNumberOnChain, getLatestBlockNumberInDB, getEtherscanGetSourceCodeResponse, getContractInfo

#OK
#print(getLatestBlockNumberOnChain())
#print(getLatestBlockNumberInDB())

#OK
#print(getEtherscanGetSourceCodeResponse("0x2E307704EfaE244c4aae6B63B601ee8DA69E92A9").json())

#OK
print(getContractInfo("0xaEcB0C976A6560270A2bace07aa230b25cd33490"))
