const axios = require('axios');

async function main() {
    var options = {
        'method': 'POST',
        'url': 'https://qianfan.baidubce.com/v2/chat/completions',
        'headers': {
                'Content-Type': 'application/json',
                'appid': 'bce-v3/ALTAK-3mgufsYhYVaiCZ6UmJMfD/037faf37d2c48b1c77f234abdce5e29337371713',
                'Authorization': 'Bearer '
        },
        data: JSON.stringify({
                "model": "ernie-4.0-turbo-8k",
                "messages": [
                        {
                                "role": "user",
                                "content": "您好"
                        }
                ],
                "web_search": {
                        "enable": false,
                        "enable_citation": false,
                        "enable_trace": false
                }
        })

    };

    axios(options)
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            throw new Error(error);
        })
}

main();
