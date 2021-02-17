



# relevant evidence question
evidencelist = ["Violation from analysis of Interviews with Involved Individuals?", "Violation from analysis of relevant collected system data?","Violation from Analysis of Incident Reports"]


# get all evidence questions

def getall_evidences():
    resultlist = []
    a = 0
    for ev in evidencelist: 
         a += 1
         evidence_obj = {}
         evidence_obj["id"] = "ev" + str(a)
         evidence_obj["question"] = ev
         resultlist.append(evidence_obj)
    return resultlist


# test
print (getall_evidences()) 
