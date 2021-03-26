const fetch = require('node-fetch')
const csv = require('csvtojson')
const mammoth = require('mammoth')
const NodeCache = require( "node-cache" );
const resourceCache = new NodeCache({stdTTL: 300});
const XLSX = require('xlsx')

exports.getPFD = (req, res) => {
    let URLData = req.query.DataURL

    if (resourceCache.has(URLData))
    {
        console.log("Cache Hit On " + URLData)
        res.setHeader("Content-Type", 'application/pdf');
        res.setHeader("Content-URL", URLData)
        res.send(resourceCache.get(URLData))
    }
    else
    {
        fetch(URLData)
        .then(res => res.buffer())
        .then(buffer => {
            if(buffer.length > 0)
            {
                res.setHeader("Content-Type", 'application/pdf');
                res.setHeader("Content-URL", URLData)
    
                if (resourceCache.set(URLData, buffer))
                {
                    res.send(buffer)
                }      
            }
            else 
            {
                res.setHeader("Content-URL", req.query.DataURL)
                res.json({Error: `Data Unavailable at ${URLData}`})
            }
        })
        .catch(err => {
            console.log(err)
        })
    }
}

exports.getDOCX = (req, res) => {
    let URLData = req.query.DataURL

    if (resourceCache.has(URLData))
    {
        console.log("Cache Hit On " + URLData)
        res.setHeader("Content-Type", 'text/html');
        res.setHeader("Content-URL", URLData)
        res.send(resourceCache.get(URLData))
    }
    else
    {
        fetch(URLData)
        .then(res => res.buffer())
        .then(buffer => {
            if(buffer.length > 0)
            {
                res.setHeader("Content-Type", 'text/html');
                res.setHeader("Content-URL", URLData)

                mammoth.convertToHtml({'buffer': buffer})
                .then(result => {
                    if (resourceCache.set(URLData, result.value))
                    {
                        res.send(result.value)
                    }    
                })
            }
            else 
            {
                res.setHeader("Content-URL", req.query.DataURL)
                res.json({Error: `Data Unavailable at ${URLData}`})
            }
        })
        .catch(err => {
            console.log(err)
        })
    }
}

exports.getXLS = (req, res) => {
    let URLData = req.query.DataURL

    if (resourceCache.has(URLData))
    {
        console.log("Cache Hit On " + URLData)
        res.setHeader("Content-URL", URLData)
        res.send(resourceCache.get(URLData))
    }
    else
    {
        fetch(URLData)
        .then(res => res.arrayBuffer())
        .then(buffer => {
            res.setHeader("Content-URL", URLData)
            let wb = XLSX.read(buffer, {type:"array"})
            let xlsRes = {}
            wb.SheetNames.forEach(sheetName => {
                xlsRes[sheetName] = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], {raw:false, header:1})
            })
            if (resourceCache.set(URLData, xlsRes))
            {
                res.send(xlsRes)
            }      
            else 
            {
                console.log("Mems")
                res.setHeader("Content-URL", URLData)
                res.json({Error: `Data Unavailable at ${URLData}`})
            }
        })
        .catch(err => {
            console.log(err)
        })
    }
}

exports.getCSV = (req, res) => {
    let URLData = req.query.CSVURL

    if (resourceCache.has(URLData))
    {
        console.log("Cache Hit On " + URLData)
        res.setHeader("Content-URL", URLData)
        res.send(resourceCache.get(URLData))
    }
    else
    {
        fetch(URLData)
        .then(res => res.text())
        .then(body => {
            csv().fromString(body)
            .then(json => {
    
                let data = {
                    rows: [],
                    columns: []
                }
    
                for(let k in json[0])
                {
                    data.columns.push({
                        label: k.toUpperCase(),
                        field: k,
                        sort: false
                    })
                }
                data.rows = json.slice(0,25); // Send first 25 rows only
    
                if (resourceCache.set(URLData, data))
                {
                    res.send(data)
                }      
            })
        })
        .catch(err => {
            console.log(err)
        })
    }
}
