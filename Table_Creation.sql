select * from  public.ecommerce_data



select *  from   preprocessed_ecommerce_data

select * from  aggregated_ecommerce_data


truncate table public.ecommerce_data
 preprocessed_ecommerce_data
  aggregated_ecommerce_data
  
  
  
 CREATE TABLE ecommerce_data (
    event_time TIMESTAMP NULL,
    event_type VARCHAR(255) NULL,
    product_id INTEGER NULL,
    category_id BIGINT NULL,
    category_code VARCHAR(255) NULL,
    brand VARCHAR(255) NULL,
    price DOUBLE PRECISION NULL,
    user_id INTEGER NULL,
    user_session VARCHAR(255) NULL
)



CREATE TABLE preprocessed_ecommerce_data (
    event_time TIMESTAMP NULL,
    event_type VARCHAR(255) NULL,
    product_id INTEGER NULL,
    category_id BIGINT NULL,
    category_code VARCHAR(255) NULL,
    brand VARCHAR(255) NULL,
    price DOUBLE PRECISION NULL,
    user_id INTEGER NULL,
    user_session VARCHAR(255) NULL
)


CREATE TABLE aggregated_ecommerce_data (
    category_id BIGINT NOT NULL,
    event_count BIGINT NOT NULL,
    avg_price DOUBLE PRECISION NOT NULL
)


