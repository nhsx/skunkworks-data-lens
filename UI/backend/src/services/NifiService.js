const fetch = require('node-fetch');

exports.uploadRequest = async (request) => {
    const response = await fetch(process.env.NIFI_INGEST_URL, {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      })
    if(response.status !== 202){
      throw new Error("Unsuccessful ingest")
    }
}

exports.uploadFileRequest = async (fileLocation, case_id) => {
  const response = await fetch(`${process.env.NIFI_FILE_INGEST_URL}file`, {
      method: 'POST',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        fileLocation,
        case_id
      })
  })

  if(response.status !== 202){
    throw new Error("Unsuccessful ingest")
  }
}