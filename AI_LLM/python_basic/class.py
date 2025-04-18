class Book:
    """ 图书类 """
    def __init__(self, title="", author="", genre=""):
        """ 初始化属性 """
        self.title = title    # 使用传入的参数值
        self.author = author  # 使用传入的参数值
        self.genre = genre  
    
    def description(self):
        """ 描述图书 """
        return f"《{self.title}》是{self.author}创作的{self.genre}类图书。"
    
    def __str__(self):
        """ 打印图书信息 """
        return f"《{self.title}》"
    
    
book = Book('Python编程', '张三', '计算机')

print(book.title)
print(book.author)
print(book.genre)
print(book.description())

# 继承

class Novel(Book):
    """ 小说类 """
    def __init__(self, title, author, genre, word_count):
        """ 初始化父类属性 """
        super().__init__(title, author, genre)
        self.word_count = word_count

    def description(self):
        """ 重写父类方法 """
        return f"《{self.title}》是{self.author}创作的{self.genre}类小说，字数为{self.word_count}字。"

    def __str__(self):
        """ 重写父类方法 """
        return f"《{self.title}》"
    

novel = Novel('Python编程', '张三', '计算机', 1000)

print(novel.title)
print(novel.author)
print(novel.genre)
print(novel.word_count)
print(novel.description())
print(novel)