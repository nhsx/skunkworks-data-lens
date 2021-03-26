import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
import groovy.json.*

def flowFile = session.get()
if (!flowFile) return


def lowerJsonCase(List source){
      def List targetList = []

      for(item in source){
        if(item instanceof String || item instanceof Integer && item.value != null && item.value != "" ){
          targetList.add(item)
        } else if(item instanceof Map){
          targetList.add(lowerJsonCase(item))
        } else if(value != null && value != ""){
            targetList.add(lowerJsonCase(item))
          }
      }
    return targetList
}

def lowerJsonCase(Map source ){
  HashMap targetMap = new HashMap()

  source.each{
    def key = it.key
    def value =it.value
    def lowerCaseKey = key.toLowerCase()

    if(value instanceof List){
      def List list = lowerJsonCase(value)
      if(list.size() != 0){
       targetMap.put("$lowerCaseKey", list)
      }
    } else if(value instanceof Map){
      processed_map = lowerJsonCase(value)
      if (! processed_map.isEmpty()){
            targetMap.put("$lowerCaseKey", lowerJsonCase(value))
      }
    } else if(value != null && value != ""){
      targetMap.put("$lowerCaseKey", value)
    }
  }
  return targetMap
}

try {
  flowFile = session.write(flowFile,
      { inputStream, outputStream ->
          def text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
          def obj = new JsonSlurper().parseText(text)

          // Output updated JSON
          def json = JsonOutput.toJson(lowerJsonCase(obj))
          outputStream.write(JsonOutput.prettyPrint(json).getBytes(StandardCharsets.UTF_8))
      } as StreamCallback)
  session.transfer(flowFile, REL_SUCCESS)

} catch(Exception e) {
  log.error('Error during JSON operations', e)
  session.transfer(flowFile, REL_FAILURE)
}
