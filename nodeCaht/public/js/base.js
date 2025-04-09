// script.js  
$(document).ready(function () {
    $('#chat-form').submit(function (e) {
        e.preventDefault();

        var message = $('#user-input').val();
        if (message.trim() !== '') {
            var $newMessage = $('<li class="user-message">' + message + '</li>');
            $('.chat-messages').append($newMessage);
            $('#user-input').val(''); // 清空输入框  
			
			//正在思考中 loading
            var loadingMsg = $('<li class="bot-message">正在思考中...</li>');
            $('.chat-messages').append(loadingMsg);
			
			 //滚动条滚动到最底部
			 $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
             // ajax post 提交数据
             $.post('/chat', { message: message }, function (data) {
                 console.log(data);
                 var $botMessage = $('<li class="bot-message">' + data.message + '</li>');
                $('.chat-messages').append($botMessage);
				 //滚动条滚动到最底部
				$('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
             })
            // 模拟机器人回复  
            // setTimeout(function () {
				
			// 	loadingMsg.remove(); // 移除loading
				  
            //     var botResponse = "Bot: " + Math.random().toString(36).substring(2, 15) + " 🤖";
            //     var $botMessage = $('<li class="bot-message">' + botResponse + '</li>');
            //     $('.chat-messages').append($botMessage);
			// 	 //滚动条滚动到最底部
			// 	$('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);

            // }, 1000);

            // 如果有真实的API，这里可以发送请求并处理响应  
        }
    });
});