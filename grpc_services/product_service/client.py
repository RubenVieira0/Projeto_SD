import grpc
import product_service_pb2
import product_service_pb2_grpc
import logging

logging.basicConfig(level=logging.INFO)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = product_service_pb2_grpc.ProductServiceStub(channel)
        
        # Health Check
        health_response = stub.GetHealth(product_service_pb2.GetProductsRequest())
        logging.info(f"Health Check: Status: {health_response.status}, Version: {health_response.version}")
        
        # Add a product
        new_product = product_service_pb2.Product(name="Test Product", price=9.99, description="A test product")
        add_response = stub.AddProduct(product_service_pb2.AddProductRequest(product=new_product))
        logging.info(f"Add Product: {add_response.message}")

        # Get all products
        products_response = stub.GetProducts(product_service_pb2.GetProductsRequest())
        logging.info(f"Got {len(products_response.products)} products:")
        for product in products_response.products:
            logging.info(f"  ID: {product.id}, Name: {product.name}, Price: {product.price}")

        # Test error handling
        invalid_product = product_service_pb2.Product(name="", price=-1)
        try:
            stub.AddProduct(product_service_pb2.AddProductRequest(product=invalid_product))
        except grpc.RpcError as e:
            logging.error(f"RPC error: {e.code()}, {e.details()}")

if __name__ == '__main__':
    run()