const env = require('node-env-file');
const express = require('express');
const app = express();
const server = require('http').Server(app)
const io = require('socket.io')(server, {
    cors: {
        origins: ['http://localhost:4200', 'https://calenbell.web.app']
    }
});
const jwt = require('jsonwebtoken');

let UsersList = [];

env(__dirname + '/.env');

io.on('connection', (socket) => {

    /***
     * @TODO Get token. Disconnect user when token is null (not authorized)
     */

    const { token } = socket.handshake.query || null;

    token == null ? socket.disconnect(force = true) : true

    /***
     * @TODO Verify Token. Add user_id and socket_id to list
     */

    jwt.verify(token, process.env.SECRET_KEY, function (err, decoded) {

        try {
            decoded.user_id === undefined ? socket.disconnect(force = true) : true;

            /***
            * @TODO Get user_id from JWT and set in list users with socket-ID
            */

            const user_id = String(decoded.user_id);

            UsersList.push(
                {
                    user_id,
                    socket_id: socket.id
                }
            );

        } catch (error) {
            /***
            * @TODO Disconnect user because token is invalid
            */

            err ? socket.disconnect(force = true) : true;
        }

        /***
         * @TODO Disconnect user because token is invalid
         */

        err ? socket.disconnect(force = true) : true;

    });

    /***
     * @TODO Listen messages
     */

    socket.on('message-one-one', (res) => {
        const { data } = res;
        const message = String(data.message);
        const token = data.token;

        /***
        * @TODO Verify if token exists else disconnect user
        */
        token == undefined ? socket.disconnect(force = true) : true;

        /***
        * @TODO Verify if message exists else disconnect user
        */
        message == undefined ? socket.disconnect(force = true) : true;

        /***
        * @TODO Verify if message is in the max range and min range else disconnect user
        */
        message.trim().lenght > 250 || message.toString().trim().lenght == 0 ? socket.disconnect(force = true) : true;

        /***
        * @TODO Verify Token. Verify errors. Verify (transmitter and receiver) if is are friends. Emit message if exist user with socket id. ELSE disconnect user.
        */
        jwt.verify(token, process.env.SECRET_KEY, function (err, decoded) {

            if (err) {
                /***
                 * @TODO Disconnect user because token is invalid
                 */
                socket.disconnect(force = true);
            };

            decoded == undefined ? socket.disconnect(force = true) : true;

            const friends = Boolean(decoded.data.friends);

            friends == false ? socket.disconnect(force = true) : true;

            const transmitter = Number(decoded.data.transmitter);
            const receiver = String(decoded.data.receiver);

            UsersList.some((user) => {
                if (user.user_id == receiver) {
                    console.log(`User ${transmitter} (${socket.id}) is sent message to ${receiver} (${user.socket_id})`);
                    return (socket.broadcast.to(user.socket_id).emit('message', { transmitter, message, type: 1 }));

                }
            });

        });

    });

    socket.on('join-group', (res) => {
        const { data } = res;

        const token = data.token;

        /***
        * @TODO Verify if token exists else disconnect user
        */
        token == undefined ? socket.disconnect(force = true) : true;

        jwt.verify(token, process.env.SECRET_KEY, function (err, decoded) {
            /***
             * @TODO Verify Token. Verify (transmitter and group) if is joined ELSE disconnect user
             */

            decoded == undefined ? socket.disconnect(force = true) : true;

            /***
             * @TODO Disconnect user because token is invalid
             */

            err ? socket.disconnect(force = true) : true;

        });
    });

    socket.on('disconnect', () => {
        /***
        * @TODO Create reference to user id. Searching socket id in users list for get user id. Delete user from users list if exists.
        */

        let user_id = null;

        UsersList.some((user) => {
            if (user.socket_id == socket.id) return (user_id = user.user_id);
        });

        UsersList = user_id != null ? UsersList.filter((user) => JSON.stringify(user) !== JSON.stringify({ "user_id": user_id, "socket_id": socket.id })) : true;

    });

});

server.listen(process.env.PORT || 3000, () => {
    console.log(`Server is running in port ${process.env.PORT || 3000}...`);
})