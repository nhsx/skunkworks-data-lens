import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
import groovy.json.*

def flowFile = session.get()
if (!flowFile) return

try {
  flowFile = session.write(flowFile,
      { inputStream, outputStream ->
          def obj = new JsonSlurper().parseText(IOUtils.toString(inputStream, StandardCharsets.UTF_8))
          List list = []

          obj.each{
            list.add(it.value)
          }

          // Output updated JSON
          def json = JsonOutput.toJson(list)
          outputStream.write(JsonOutput.prettyPrint(json).getBytes(StandardCharsets.UTF_8))
      } as StreamCallback)
  session.transfer(flowFile, REL_SUCCESS)

} catch(Exception e) {
  log.error('Error during JSON operations', e)
  session.transfer(flowFile, REL_FAILURE)
}
