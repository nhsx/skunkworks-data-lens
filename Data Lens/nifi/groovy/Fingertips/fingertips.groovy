import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import groovy.json.JsonBuilder

// get incoming FlowFile
def flowFiles = session.get(100)
if (!flowFiles) return

final JsonSlurper slurper = new JsonSlurper()

for (final def flowFile: flowFiles) {
  def profileData = ''
  def indicatorPerGroup = ''
  def indicatorMetadata


  // read in both attributes used to store API calls
  try {
    profileData = slurper.parseText(flowFile.getAttribute('profile_data'))
    indicatorPerGroup = slurper.parseText(flowFile.getAttribute('indicators_by_group'))
    indicatorMetadata = slurper.parseText(flowFile.read().getText("UTF-8"))
  } catch(Exception ex) {
    log.warn("Unable to parse as JSON to retrieve pass object: ${ex}")
  }

  //For each group in profile data loop through indicators and see if they are part of the group
  //If they are then add them to a list and then add them to that groups json.
  for (group in profileData.GroupMetadata) {
    List list = []
    for (indicator in indicatorPerGroup) {
      String indicatorId = indicator.IndicatorId

      if(indicatorMetadata."$indicatorId"."Descriptive"."Definition" != null){
        indicator.put("definition", indicatorMetadata."$indicatorId"."Descriptive"."Definition")
      }
      if(indicatorMetadata."$indicatorId"."Descriptive"."Rationale" != null){
        indicator.put("rationale", indicatorMetadata."$indicatorId"."Descriptive"."Rationale")
      }

      if (group.Id == indicator.GroupId) {
        def url = "https://fingertips.phe.org.uk/search/" + indicator.IndicatorId
        list.add(id: indicator.IndicatorId, name: indicator.IndicatorName, url: url, definition: indicator.definition, rationale: indicator.rationale)
      }
    }
    group.identifiers = list
  }


  // replace flowfile content with record
  flowFile.write("UTF-8", JsonOutput.toJson(profileData))

  // transfer flow file to success relationship
  REL_SUCCESS << flowFile
}
