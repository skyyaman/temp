import re
import json
json3 = 'jsonp1000({"code":200,"data":{"userActivityStatus":1,"continuePrizeRuleList":[{"level":7,"prizeList":[{"discount":50.00,"type":6,"prizeId":0,"number":10000,"budgetNum":500000,"userPirzeStatus":1,"class":"com.jd.interact.center.client.api.user.domain.InteractUserPrize","status":2}],"signType":1,"days":7,"class":"com.jd.interact.center.client.api.color.domain.sign.ShopSignInteractUserPrizeRule"},{"level":15,"prizeList":[{"discount":120.00,"type":6,"prizeId":0,"number":10000,"budgetNum":1200000,"userPirzeStatus":1,"class":"com.jd.interact.center.client.api.user.domain.InteractUserPrize","status":2}],"signType":1,"days":15,"class":"com.jd.interact.center.client.api.color.domain.sign.ShopSignInteractUserPrizeRule"}],"activityName":"店铺签到","activityStatus":2,"venderId":1000004701,"startTime":1647532800000,"endTime":1650038399000,"id":10810527,"class":"com.jd.interact.center.client.api.color.domain.sign.ShopSignActivity","prizeRuleList":[{"level":0,"prizeList":[{"discount":2.00,"type":6,"prizeId":0,"number":100000,"budgetNum":200000,"userPirzeStatus":1,"class":"com.jd.interact.center.client.api.user.domain.InteractUserPrize","status":2}],"class":"com.jd.interact.center.client.api.color.domain.sign.ShopSignInteractUserPrizeRule"}]},"class":"com.jd.interact.center.client.api.common.param.Results","success":true});'
res='(?<=\().*(?=\))'
jsonE=re.search(res,json3,re.M|re.I).group(0)
print(json.loads(jsonE).get('data').get('continuePrizeRuleList'))