//生成一个express应用并配置body-parser中间件和ejs模板引擎
import express from 'express';
import bodyParser from 'body-parser';
import ejs from 'ejs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
//配置body-parser中间件，用于解析请求体
app.use(bodyParser.urlencoded({ extended: true }));
//配置ejs模板引擎
app.engine('html', ejs.__express);

//设置视图引擎为html
app.set('view engine', 'html');

// 设置正确的视图目录路径
app.set('views', path.join(__dirname, '../views'));

// 设置正确的静态文件目录路径
app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
    //渲染index.html页面
    res.render('index');
});

// 以post方式接收message参数，并返回一个json对象
app.post('/chat', async (req, res) => {
    // 从请求体中获取message参数
    const message = req.body.message;

    // 在这里处理message参数，生成响应数据
    // 这里只是一个示例，你可以根据自己的需求进行处理
    const responseData = {
        message: 'Hello, ' + message
    };
    // 返回响应数据
    res.json(responseData);
}); 

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});