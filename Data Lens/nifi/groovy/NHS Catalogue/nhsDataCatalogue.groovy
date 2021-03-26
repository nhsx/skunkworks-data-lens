import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
import groovy.json. *

def flowFile = session.get()
if (!flowFile) return

def get_vectors(data) throws Exception {
  // POST
  final JsonSlurper slurper = new JsonSlurper()

  def post = new URL("http://datalens-semantic-alb-{server_id}.eu-west-2.elb.amazonaws.com/semantic/embed?target=" + data.source.replace(" ", "%20")).openConnection();
  def message = JsonOutput.toJson(data)
  post.setRequestMethod("POST")
  post.setDoOutput(true)
  post.setRequestProperty("Content-Type", "application/json")
  post.getOutputStream().write(message.getBytes("UTF-8"));
  def postRC = post.getResponseCode();
  if (postRC.equals(200)) {
    return slurper.parseText(post.getInputStream().getText())
  } else {
        log.warn("Vector request failed. Returned code: " + postRC.toString() + ". For source: " + data.source.replace(" ", "%20") + ". Data used: " + JsonOutput.toJson(data))
  }
}

def get_entities(data, fields) throws Exception {
  def entity_sentence = ""
  for (field in fields) {
    if (field in data) {
      entity_sentence += data[field]
    }
  }

  final JsonSlurper slurper = new JsonSlurper()

  // POST
  def post = new URL("https://{server_id}.execute-api.eu-west-2.amazonaws.com/entities").openConnection();
  def message = JsonOutput.toJson(entity_sentence)
  post.setRequestMethod("POST")
  post.setDoOutput(true)
  post.setRequestProperty("Content-Type", "application/json")
  post.getOutputStream().write(message.getBytes("UTF-8"));
  def postRC = post.getResponseCode();
  if (postRC.equals(200)) {
    return slurper.parseText(post.getInputStream().getText())
  } else {
       log.warn("Entity request failed code: " + postRC.toString() + " Data used: " + entity_sentence)
  }
}

try {
  flowFile = session.write(flowFile, {
    inputStream, outputStream ->
    def text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    def record = new JsonSlurper().parseText(text)

    def coverage_end_date = record.coverage_end_date
    def coverage_start_date = record.coverage_start_date


    String regex1 = /((\d\d\d\d)-(\d\d)-(\d))/
    String regex2 = /((\d\d\d\d)-(\d)-(\d))/
    String regex3 = /((\d\d\d\d)-(\d)-(\d\d))/


    /////// ADD URL FOR CATALOGUE
    if (record.name != null || record.name != "") {
      record.url = "https://data.england.nhs.uk/dataset/${record.name}"
    }

    record.source = "NHS Data Catalogue"
    record.source_url = "https://data.england.nhs.uk"

    /////// STANDARDISES COVERAGE DATES
    if (coverage_end_date == null || coverage_end_date.isEmpty()) {
      record.remove('coverage_end_date')
    } else if (coverage_end_date ==~ regex1) {
      record.coverage_end_date = coverage_end_date.substring(0, 8) + "0" + coverage_end_date.substring(8, 9)
    } else if (coverage_end_date ==~ regex2 || coverage_end_date ==~ regex3) {
      record.coverage_end_date = coverage_end_date.substring(0, 5) + "0" + coverage_end_date.substring(5, 9)
    }

    if (coverage_start_date == null || coverage_start_date.isEmpty()) {
      record.remove('coverage_start_date')
    } else if (coverage_start_date ==~ regex1) {
      record.coverage_start_date = coverage_start_date.substring(0, 8) + "0" + coverage_start_date.substring(8, 9)
    } else if (coverage_start_date ==~ regex2 || coverage_start_date ==~ regex3) {
      record.coverage_start_date = coverage_start_date.substring(0, 5) + "0" + coverage_start_date.substring(5, 9)
    }

    record.vectors = get_vectors(record)

    record.entities = get_entities(record, ["title"])

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