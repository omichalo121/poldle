const express = require('express');

const { exec } = require('child_process');
const crypto = require('crypto');

const app = express();

const GITHUB_SECRET = '%#GTYRh745y7rGTFD^#4fstdrTYGDRTF$%fdegtydrgtdrft4234432crfERDRTFER543';
const DEBUG_PREFIX = '[WEBHOOK]'
const REFRESH_COMMAND = 'sh -c "docker compose stop && docker compose build --no-cache && docker compose up -d"';

app.use(express.json());

app.post('/github/refresh', (req, res) => {
    const sha1sum = crypto.createHash('sha1');
    sha1sum.update(GITHUB_SECRET);

    const sha1hash = `sha1=${sha1sum.digest('hex')}`;

    const agent = req.header('User-Agent');
    const event = req.header('X-GitHub-Event');
    const delivery = req.header('X-GitHub-Delivery');
    const signature = req.header('X-Hub-Signature');
    const signature256 = req.header('X-Hub-Signature-256');

    const payload = req.body;

    console.log(`User Agent: ${agent}`);
    console.log(`Event: ${event}`);
    console.log(`Delivery: ${delivery}`);
    console.log(`Signature: ${signature}`);
    console.log(`Signature 256: ${signature256}`);

    console.log(`SHA1 DIGEST: ${sha1hash}`);

    console.log(payload);

    if (payload != null && payload.ref === 'refs/heads/main') {
        console.log(`${DEBUG_PREFIX} Detected MAIN change - restarting container`);

        exec(REFRESH_COMMAND, (err, stdout, stderr) => {

            if (err) {
                console.error(`${DEBUG_PREFIX} ${err}`);
                res.status(500).send('ERR');
            }
            else if (stderr) {
                console.error(`${DEBUG_PREFIX} ${err}`);
                res.status(500).send('ERR');
            }
            else {
                console.log(`${DEBUG_PREFIX} ${stdout}`);
                res.status(200).send('THX');
            }
        });
    }
    else {
        console.log(`${DEBUG_PREFIX} Not MAIN change - skipping`);
        res.status(200).send('THX');
    }
});

app.listen(8000, _ => {
    console.log(`${DEBUG_PREFIX} Listening for incoming events from Github`);
});
