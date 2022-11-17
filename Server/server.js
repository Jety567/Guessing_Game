const express = require('express');
const jsonServer = require('json-server');
const axios = require('axios');

const server = express();

server.use('/api', jsonServer.router('db.json'));
server.use(express.json());


server.post('/highscore/:game/:level',async (req, res) => {
    try {
        let request = await axios.get(`http://localhost:3000/api/highscore?name=${req.body.name}&points=${req.body.points}&game=${req.params.game}&level=${req.params.level}`);
        if(request.data.length > 0)
            return res.sendStatus(200);

        let data = {
            name: req.body.name,
            points: req.body.points,
            game: req.params.game,
            level: req.params.level,
            creatdAt: Date.now(),
        }
        console.log(data);
        await axios.post('http://localhost:3000/api/highscore',data);
        return res.sendStatus(200);
    }catch (e) {
        console.log(e);
        res.sendStatus(500);
    }
})

server.get('/highscore/:game/:level',async (req,res) => {
    try {
        let data = await axios.get(`http://localhost:3000/api/highscore?game=${req.params.game}&level=${req.params.level}`);
        let array = data.data;
        array.sort(function(a, b) {
            let keyA = new Date(a.points);
            let keyB = new Date(b.points);

            if (keyA > keyB)
                return -1;
            if (keyA < keyB)
                return 1;

            return 0;
        });
    res.json(array.slice(0,7));
    }catch (e) {
        console.log(e);
        res.sendStatus(500);
    }
});

server.listen(3000,() => {

});