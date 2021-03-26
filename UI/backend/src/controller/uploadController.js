const { readdirSync, existsSync} = require('fs')
const { uploadRequest, uploadFileRequest } = require('../services/NifiService');

exports.getUploadItems = async(req, res, next) => {
    try{
        const directories = readdirSync(process.env.INGEST_DIRECTORY, { withFileTypes: true })
            .filter(item => item.isDirectory())
            .filter(item => existsSync(`${process.env.INGEST_DIRECTORY}/${item.name}/report.xml`))
            .map(item => item.name)
            
        res.send(directories)
    } catch(error) {
        next(error)
    }
}

exports.upload = async(req, res, next) => {
    try{
        const nifiRequest = {
            ...req.body
        }
        res.send(await uploadRequest(nifiRequest) ? "Success" : "failure");
    } catch(error) {
        next(error)
    }
}

exports.uploadFile = async(req, res, next) => {
    try{
        const filePath = `${process.env.INGEST_DIRECTORY}/${process.env.FILE_UPLOAD_DIR}/${req.files.file.name}`
        req.files.file.mv(filePath)
        await uploadFileRequest(`${process.env.FILE_UPLOAD_DIR}/${req.files.file.name}`, req.body['case_id']);
        res.send('ok')
    } catch(error) {
        next(error)
    }
}
  