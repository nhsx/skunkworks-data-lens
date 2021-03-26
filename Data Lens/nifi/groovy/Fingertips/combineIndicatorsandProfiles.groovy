import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
import groovy.json.*
import groovy.transform.Field

def flowFile = session.get()
if (!flowFile) return


@Field JsonSlurper json_parser = new JsonSlurper()

def get_vectors(data) {
  // POST
  def post = new URL("http://datalens-semantic-alb-{server_id}.eu-west-2.elb.amazonaws.com/semantic/embed?target=" + data.source.replace(" ", "%20")).openConnection();
  def message = JsonOutput.toJson(data)
  post.setRequestMethod("POST")
  post.setDoOutput(true)
  post.setRequestProperty("Content-Type", "application/json")
  post.getOutputStream().write(message.getBytes("UTF-8"));
  def postRC = post.getResponseCode();
  if (postRC.equals(200)) {
    return json_parser.parseText(post.getInputStream().getText())
  } else {
        log.warn("Vector request failed. Returned code: " + postRC.toString() + ". For source: " + data.source.replace(" ", "%20") + ". Data used: " + JsonOutput.toJson(data))
  }
}

def get_entities(data, fields) {
  def entity_sentence = ""
  for (field in fields) {
    if (field in data) {
      entity_sentence += data[field]
    }
  }

  // POST
  def post = new URL("https://bf58t6f3uh.execute-api.eu-west-2.amazonaws.com/entities").openConnection();
  def message = JsonOutput.toJson(entity_sentence)
  post.setRequestMethod("POST")
  post.setDoOutput(true)
  post.setRequestProperty("Content-Type", "application/json")
  post.getOutputStream().write(message.getBytes("UTF-8"));
  def postRC = post.getResponseCode();
  if (postRC.equals(200)) {
    return json_parser.parseText(post.getInputStream().getText())
  } else {
       log.warn("Entity request failed code: " + postRC.toString() + " Data used: " + entity_sentence)
  }
}

try {
  flowFile = session.write(flowFile, {
    inputStream,
    outputStream ->

    def profileData = ''
    def indicatorPerGroup = ''
    def indicatorMetadata

    // read in data
    try {
      record = json_parser.parseText(flowFile.getAttribute('indicatorData'))
      profile_data = json_parser.parseText(IOUtils.toString(inputStream, StandardCharsets.UTF_8))
    } catch(Exception ex) {
      log.warn("Unable to parse as JSON to retrieve pass object: ${ex}")
    }

    // go through profiles for the indicator and add them to a list then add the list to the data.
    def List profileList = []
    def indicatorId = record.IID

    /*
    Data is split into 2 API calls that have happened in the nifi flow 1 is stored as an attribute, the other as the
    flowfile content. The record we want to pass to elastic is the one stored as an attribute, however, we want to add
    data from the other.
    */
    for (item in profile_data."${indicatorId}") {
      profileList.add item
    }

    // Bring nested items upwards and remove the old object.
    for (item in record.Descriptive) {
      record.put(item.key, item.value)
    }

    record.remove('Descriptive')

    // Add data + rename some keys
    record.profiles = profileList
    record.url = "https://fingertips.phe.org.uk/search/" + record.IID
    record.source = "PHE Fingertips"
    record.source_url = "https://fingertips.phe.org.uk"
    record.title = record.Name
    record.remove('Name')
    record.indicatorId = record.IID
    record.remove('IID')
    record.vectors = get_vectors(record)
    record.entities = get_entities(record, ["Title"])

    // Output updated JSON
    def json = JsonOutput.toJson(record)
    outputStream.write(JsonOutput.prettyPrint(json).getBytes(StandardCharsets.UTF_8))
  }
  as StreamCallback)
  session.transfer(flowFile, REL_SUCCESS)

} catch(Exception e) {
  log.error('Exception: ', e)
  session.transfer(flowFile, REL_FAILURE)
}