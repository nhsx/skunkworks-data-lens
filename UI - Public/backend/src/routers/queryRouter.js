const express = require('express');
const router = express.Router();
const elasticController = require('../controller/elasticController');
const previewRequests = require('../utils/PreviewRequests')

router.post('/query', elasticController.simpleQuery);
router.post('/clicklog', elasticController.addClickLog);

router.get('/search/:id', elasticController.searchById);

router.get(`/getPDF`, previewRequests.getPFD)
router.get('/getCSV', previewRequests.getCSV)
router.get('/getXLS', previewRequests.getXLS)
router.get('/getDOCX', previewRequests.getDOCX)

module.exports = router;
