from flask import request, jsonify
from CreateServiceCategoryController import CreateServiceCategoryController
from UpdateServiceCategoryController import UpdateServiceCategoryController
from DeleteServiceCategoryController import DeleteServiceCategoryController
from SearchServiceCategoryController import SearchServiceCategoryController
from ServiceCategory import ServiceCategory

def register_service_category_routes(app):

    # Create service category
    @app.route("/api/service_categories", methods=["POST"])
    def create_service_category():
        data = request.json
        category_name = data.get("CategoryName")

        if not category_name:
            return jsonify({"error": "Missing CategoryName"}), 400

        result = ServiceCategory.createServiceCategory(category_name)
        return jsonify({"message": "Service category created successfully"}), 201

    # View all service categories (with optional search)
    @app.route("/api/service_categories", methods=["GET"])
    def get_service_categories():
        search_query = request.args.get("search")
        categories = ServiceCategory.searchcategory(search_query)
        return jsonify(categories)

    # Update service category
    @app.route("/api/service_categories/<string:CategoryName>", methods=["PUT"])
    def update_service_category(CategoryName):
        data = request.json
        new_name = data.get("CategoryName")

        if not new_name:
            return jsonify({"error": "Missing new CategoryName"}), 400

        result, status = ServiceCategory.update_service_category(new_name)
        return jsonify(result), status

    # Delete service category
    @app.route("/api/service_categories/<string:CategoryName>", methods=["DELETE"])
    def delete_service_category(CategoryName):
        result, status = ServiceCategory.delete_by_category(CategoryName)
        return jsonify(result), status

    # Search service categories (alternate path)
    @app.route("/api/service_categories/search", methods=["GET"])
    def search_service_categories():
        search_query = request.args.get("search", "").strip()
        categories = ServiceCategory.searchcategory(search_query)
        return jsonify(categories)