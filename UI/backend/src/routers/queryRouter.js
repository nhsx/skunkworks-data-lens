const express = require('express');
const router = express.Router();
const elasticController = require('../controller/elasticController');
const uploadController = require('../controller/uploadController');
const previewRequests = require('../utils/PreviewRequests')

router.post('/query', elasticController.simpleQuery);
router.post('/query/bulk', elasticController.bulkQuery);
router.post('/clicklog', elasticController.addClickLog);

router.get('/search/:id', elasticController.searchById);
router.post('/query/custom/:index', elasticController.customQuery);

router.get('/upload', uploadController.getUploadItems);
router.post('/upload', uploadController.upload);
router.post('/upload/file', uploadController.uploadFile);

router.get(`/getPDF`, previewRequests.getPFD)
router.get('/getCSV', previewRequests.getCSV)
router.get('/getXLS', previewRequests.getXLS)
router.get('/getDOCX', previewRequests.getDOCX)

module.exports = router;
