# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy import settings
from scrapy.utils.project import get_project_settings

class BookschinaPipeline:
    def process_item(self, item, spider):
        return item
class MySQLPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.items_buffer = []  # 用于存储待批量插入的数据
        self.batch_size = 20   # 每n条数据批量插入一次
        self.insert_count = 0   # 记录已插入的数据数量
    def open_spider(self,spider):
        settings = get_project_settings()
        self.conn = pymysql.connect(host=settings.get('MYSQL_HOST'),
        user=settings.get('MYSQL_USER'),
        password=settings.get('MYSQL_PASSWORD'),
        database=settings.get('MYSQL_DATABASE'),
        charset=settings.get('CHARSET'),
        port=settings.get('MYSQL_PORT'))
        self.cursor = self.conn.cursor()
    def close_spider(self,spider):
        if self.items_buffer:
            self._batch_insert(spider)
            
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        
        spider.logger.info(f"爬取完成，共插入 {self.insert_count} 条数据到数据库")
    def _batch_insert(self, spider):
        """批量插入数据到MySQL"""
        if not self.items_buffer:
            return
        
        try:
            # 准备批量插入的SQL语句
            insert_sql = """
            INSERT INTO books_tb (
                book_id, title, free_shipping, author, price, one_star_price, 
                three_star_price, discount, reader_ratings, rating_num, 
                is_stock, level_1_category, level_2_category, publisher, 
                publish_date, ranking, ranking_num
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=VALUES(title), free_shipping=VALUES(free_shipping), author=VALUES(author), 
                price=VALUES(price), one_star_price=VALUES(one_star_price), 
                three_star_price=VALUES(three_star_price), discount=VALUES(discount),
                reader_ratings=VALUES(reader_ratings), rating_num=VALUES(rating_num), 
                is_stock=VALUES(is_stock), level_1_category=VALUES(level_1_category), 
                level_2_category=VALUES(level_2_category), publisher=VALUES(publisher),
                publish_date=VALUES(publish_date), ranking=VALUES(ranking), 
                ranking_num=VALUES(ranking_num)
            """
            
            # 执行批量插入
            self.cursor.executemany(insert_sql, self.items_buffer)
            self.conn.commit()
            
            # 更新计数并清空缓冲区
            inserted_count = len(self.items_buffer)
            self.insert_count += inserted_count
            spider.logger.info(f"------成功批量插入 {inserted_count} 条数据，累计: {self.insert_count} 条---------")
            self.items_buffer = []
            
        except Exception as e:
            spider.logger.error(f"MySQL批量存储错误: {e}")
            self.conn.rollback()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # 准备数据元组（只需要17个值，使用VALUES()函数引用插入的值）
        data = (
            adapter.get('book_id', ''),
            adapter.get('title', ''),
            adapter.get('free_shipping', ''),
            adapter.get('author', ''),
            adapter.get('price', ''),
            adapter.get('one_star_price', ''),
            adapter.get('three_star_price', ''),
            adapter.get('discount', ''),
            adapter.get('reader_ratings', ''),
            adapter.get('rating_num', ''),
            adapter.get('is_stock', ''),
            adapter.get('level_1_category', ''),
            adapter.get('level_2_category', ''),
            adapter.get('publisher', ''),
            adapter.get('publish_date', ''),
            adapter.get('ranking', ''),
            adapter.get('ranking_num', '')
        )
        
        # 将数据添加到缓冲区
        self.items_buffer.append(data)
        
        # 当缓冲区达到指定大小时，执行批量插入
        if len(self.items_buffer) >= self.batch_size:
            self._batch_insert(spider)
        
        return item