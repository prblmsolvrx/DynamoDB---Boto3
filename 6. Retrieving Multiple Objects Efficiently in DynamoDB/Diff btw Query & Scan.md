In DynamoDB, `Query` and `Scan` are two distinct operations used to retrieve data from tables, and they have different use cases and performance implications.

### **Query**

- **Purpose**: Retrieves items from a table or index based on a specific condition, primarily using the primary key (partition key) or a composite key (partition key and sort key).

- **Efficiency**: More efficient than `Scan` because it uses indexes and is designed to retrieve only the items that match the specified criteria. It can be very fast when used with primary key values or indexed attributes.

- **Performance**: It only reads the items that match the query criteria, so it consumes fewer read capacity units (RCUs) and is generally faster.

- **Usage**: Ideal for scenarios where you need to retrieve a subset of items based on known key values or indexed attributes.

- **Example**: Retrieve all orders for a specific customer.

  ```python
  response = table.query(
      KeyConditionExpression=Key('customer_id').eq('12345')
  )
  ```

### **Scan**

- **Purpose**: Examines every item in a table or index and retrieves all the data that matches the filter criteria. It can be used to scan the entire table or index.

- **Efficiency**: Less efficient than `Query` because it reads every item in the table or index and then applies the filter criteria. This can be expensive and slow, especially for large tables.

- **Performance**: Can consume a lot of read capacity units (RCUs) and may lead to higher costs and slower response times.

- **Usage**: Useful for scenarios where you need to retrieve data based on attributes that are not part of the primary key or indexes. It is also useful for operations like data migration or analysis.

- **Example**: Retrieve all items where the status attribute is 'active'.

  ```python
  response = table.scan(
      FilterExpression=Attr('status').eq('active')
  )
  ```

### **Key Differences**

- **Efficiency**: `Query` is generally more efficient because it uses indexes and reads only the items that match the key condition. `Scan` is less efficient as it scans the entire table or index and then filters results.

- **Read Capacity**: `Query` uses fewer read capacity units compared to `Scan`, especially when working with large datasets.

- **Use Cases**: Use `Query` when you need to retrieve items based on primary keys or indexed attributes. Use `Scan` for broader searches or when dealing with non-indexed attributes.

Understanding these differences can help you design more efficient data retrieval strategies for your DynamoDB tables.