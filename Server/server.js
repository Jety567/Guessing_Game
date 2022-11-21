const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const jsonServer = require('json-server');
const axios = require('axios');

const { Server } = require("socket.io");
const io = new Server(server);

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('join_room',() => {
     console.log("Join Room")
  });
  socket.on('Client:get_rooms',() => {
      emit_rooms();

  })

  socket.on('Client:new_room',(args) => {
      if(io.of('/').adapter.rooms.has(`Client_${args.room_name}`))
          return socket.emit('Server:room_exits',args.room_name);

      socket.join(`Client_${args.room_name}`);

      socket.emit('Server:room_created',{
         name: args.room_name,
      });
      emit_rooms();
  });

  socket.on('Client:leave_room',(args) => {
      console.log(args);
      socket.leave(args);
  });

  socket.on('Client:join_room',(args) => {

  })

});


app.use('/api', jsonServer.router('db.json'));
app.use(express.json());


app.post('/highscore/:game/:level',async (req, res) => {
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

        await axios.post('http://localhost:3000/api/highscore',data);
        return res.sendStatus(200);
    }catch (e) {
        console.log(e);
        res.sendStatus(500);
    }
})

app.get('/highscore/:game/:level',async (req,res) => {
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

const emit_rooms = () => {
    let rooms = io.of('/').adapter.rooms;

    let array = Array.from(rooms.keys());


    array = array.filter((obj) => {
          return obj.includes('Client_') && rooms.get(obj).size === 1;
      })

    array = array.map((room) => {
        return room.replace('Client_','');
    })
    io.emit('Server:rooms',array);
}

server.listen(3000,() => {

});