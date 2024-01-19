fewshots = [
    {
        'Question': "how many t-shirts do we have for Nike in extra small and white color?",
        'SQLQuery': "SELECT stock_quantity FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        'SQLResult': "Result of the SQL query",
        'Answer': "82"
    },
    {
        'Question': "how much is the price of the inventory for all small size t-shirts?",
        'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        'SQLResult': "Result of the SQL query",
        'Answer': "14480"

    },
    {
        'Question': "if we have to see all my levi's t-shirts today with discounts applied. how much revenue our store will generate (post discounts)?",
        'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) AS total_revenue FROM (select sum(price*stock_quantity) AS total_amount, t_shirt_id FROM t_shirts WHERE brand = "Levi" GROUP BY t_shirt_id) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "30276"

    },
    {
        'Question': "how many white color levi's t-shirts we have available?",
        'SQLQuery': "SELECT sum(stock_quantity) FROM t-shirts WHERE brand = 'Levi' AND color = 'White'",
        'SQLResult': "Result of the SQL query",
        'Answer': "199"
    }
]