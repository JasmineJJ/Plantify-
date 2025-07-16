#!/usr/bin/env python3
"""
Comprehensive CRUD operations test for Plant Health Monitoring API
"""
import asyncio
import json
from app.core.database import init_db, close_db
from app.services.user_service import UserService
from app.services.plant_service import PlantService
from app.services.diagnosis_service import DiagnosisService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.plant import PlantCreate, PlantUpdate
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate

async def test_user_crud():
    """Test User CRUD operations"""
    print("=== TESTING USER CRUD OPERATIONS ===")
    
    # CREATE
    print("1. Testing User Creation...")
    user_data = UserCreate(email="john.doe@example.com", name="John Doe")
    user = await UserService.create_user(user_data)
    print(f"SUCCESS: Created user: {user.name} ({user.email}) - ID: {user.id}")
    
    # READ - Get by ID
    print("2. Testing User Read by ID...")
    retrieved_user = await UserService.get_user_by_id(user.id)
    print(f"✓ Retrieved user: {retrieved_user.name} - {retrieved_user.email}")
    
    # READ - Get by Email
    print("3. Testing User Read by Email...")
    user_by_email = await UserService.get_user_by_email(user.email)
    print(f"✓ Retrieved user by email: {user_by_email.name}")
    
    # UPDATE
    print("4. Testing User Update...")
    update_data = UserUpdate(name="John Doe Updated")
    updated_user = await UserService.update_user(user.id, update_data)
    print(f"✓ Updated user name: {updated_user.name}")
    
    # READ ALL
    print("5. Testing Get All Users...")
    all_users = await UserService.get_all_users()
    print(f"✓ Found {len(all_users)} users")
    
    return user

async def test_plant_crud(user):
    """Test Plant CRUD operations"""
    print("\n=== TESTING PLANT CRUD OPERATIONS ===")
    
    # CREATE
    print("1. Testing Plant Creation...")
    plant_data = PlantCreate(
        name="Rose Bush",
        species="Rosa rubiginosa",
        description="Beautiful red roses",
        user_id=user.id
    )
    plant = await PlantService.create_plant(plant_data)
    print(f"✓ Created plant: {plant.name} ({plant.species}) - ID: {plant.id}")
    
    # READ - Get by ID
    print("2. Testing Plant Read by ID...")
    retrieved_plant = await PlantService.get_plant_by_id(plant.id)
    print(f"✓ Retrieved plant: {retrieved_plant.name} - {retrieved_plant.species}")
    
    # UPDATE
    print("3. Testing Plant Update...")
    update_data = PlantUpdate(description="Beautiful red roses in the garden")
    updated_plant = await PlantService.update_plant(plant.id, update_data)
    print(f"✓ Updated plant description: {updated_plant.description}")
    
    # READ ALL
    print("4. Testing Get All Plants...")
    all_plants = await PlantService.get_all_plants()
    print(f"✓ Found {len(all_plants)} plants")
    
    # READ BY USER
    print("5. Testing Get Plants by User...")
    user_plants = await PlantService.get_plants_by_user(user.id)
    print(f"✓ Found {len(user_plants)} plants for user {user.name}")
    
    return plant

async def test_diagnosis_crud(plant):
    """Test Diagnosis CRUD operations"""
    print("\n=== TESTING DIAGNOSIS CRUD OPERATIONS ===")
    
    # CREATE
    print("1. Testing Diagnosis Creation...")
    diagnosis_data = DiagnosisCreate(
        plant_id=plant.id,
        disease_name="Black Spot",
        confidence_score=0.87,
        image_path="/uploads/plant_disease_001.jpg",
        notes="Black spots observed on leaves",
        is_healthy=False
    )
    diagnosis = await DiagnosisService.create_diagnosis(diagnosis_data)
    print(f"✓ Created diagnosis: {diagnosis.disease_name} (confidence: {diagnosis.confidence_score}) - ID: {diagnosis.id}")
    
    # READ - Get by ID
    print("2. Testing Diagnosis Read by ID...")
    retrieved_diagnosis = await DiagnosisService.get_diagnosis_by_id(diagnosis.id)
    print(f"✓ Retrieved diagnosis: {retrieved_diagnosis.disease_name} - {retrieved_diagnosis.notes}")
    
    # UPDATE
    print("3. Testing Diagnosis Update...")
    update_data = DiagnosisUpdate(
        confidence_score=0.92,
        notes="Black spots observed on leaves, treatment recommended"
    )
    updated_diagnosis = await DiagnosisService.update_diagnosis(diagnosis.id, update_data)
    print(f"✓ Updated diagnosis confidence: {updated_diagnosis.confidence_score}")
    
    # READ ALL
    print("4. Testing Get All Diagnoses...")
    all_diagnoses = await DiagnosisService.get_all_diagnoses()
    print(f"✓ Found {len(all_diagnoses)} diagnoses")
    
    # READ BY PLANT
    print("5. Testing Get Diagnoses by Plant...")
    plant_diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant.id)
    print(f"✓ Found {len(plant_diagnoses)} diagnoses for plant {plant.name}")
    
    # READ BY USER
    print("6. Testing Get Diagnoses by User...")
    user_diagnoses = await DiagnosisService.get_diagnoses_by_user(plant.user.id)
    print(f"✓ Found {len(user_diagnoses)} diagnoses for user {plant.user.name}")
    
    return diagnosis

async def test_relationships():
    """Test relationships between models"""
    print("\n=== TESTING RELATIONSHIPS ===")
    
    # Get user with plants
    users = await UserService.get_all_users()
    if users:
        user = users[0]
        plants = await PlantService.get_plants_by_user(user.id)
        print(f"✓ User {user.name} has {len(plants)} plants")
        
        if plants:
            plant = plants[0]
            diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant.id)
            print(f"✓ Plant {plant.name} has {len(diagnoses)} diagnoses")

async def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n=== TESTING EDGE CASES ===")
    
    # Test non-existent IDs
    print("1. Testing non-existent user...")
    non_existent_user = await UserService.get_user_by_id(99999)
    print(f"✓ Non-existent user returns: {non_existent_user}")
    
    print("2. Testing non-existent plant...")
    non_existent_plant = await PlantService.get_plant_by_id(99999)
    print(f"✓ Non-existent plant returns: {non_existent_plant}")
    
    print("3. Testing non-existent diagnosis...")
    non_existent_diagnosis = await DiagnosisService.get_diagnosis_by_id(99999)
    print(f"✓ Non-existent diagnosis returns: {non_existent_diagnosis}")
    
    # Test invalid foreign keys
    print("4. Testing plant creation with invalid user...")
    invalid_plant_data = PlantCreate(
        name="Invalid Plant",
        species="Invalid Species", 
        user_id=99999
    )
    invalid_plant = await PlantService.create_plant(invalid_plant_data)
    print(f"✓ Invalid user plant creation returns: {invalid_plant}")

async def test_counts():
    """Test count operations"""
    print("\n=== TESTING COUNT OPERATIONS ===")
    
    user_count = await UserService.get_users_count()
    plant_count = await PlantService.get_plants_count()
    diagnosis_count = await DiagnosisService.get_diagnoses_count()
    
    print(f"✓ Total users: {user_count}")
    print(f"✓ Total plants: {plant_count}")
    print(f"✓ Total diagnoses: {diagnosis_count}")

async def test_delete_operations():
    """Test delete operations"""
    print("\n=== TESTING DELETE OPERATIONS ===")
    
    # Get existing records to delete
    diagnoses = await DiagnosisService.get_all_diagnoses()
    plants = await PlantService.get_all_plants()
    users = await UserService.get_all_users()
    
    # Delete diagnosis
    if diagnoses:
        diagnosis = diagnoses[0]
        success = await DiagnosisService.delete_diagnosis(diagnosis.id)
        print(f"✓ Deleted diagnosis {diagnosis.id}: {success}")
    
    # Delete plant
    if plants:
        plant = plants[0]
        success = await PlantService.delete_plant(plant.id)
        print(f"✓ Deleted plant {plant.id}: {success}")
    
    # Delete user
    if users:
        user = users[0]
        success = await UserService.delete_user(user.id)
        print(f"✓ Deleted user {user.id}: {success}")

async def main():
    """Main test function"""
    print("STARTING COMPREHENSIVE CRUD TESTS")
    print("=" * 50)
    
    try:
        # Initialize database
        await init_db()
        print("✓ Database initialized")
        
        # Run tests
        user = await test_user_crud()
        plant = await test_plant_crud(user)
        diagnosis = await test_diagnosis_crud(plant)
        
        await test_relationships()
        await test_edge_cases()
        await test_counts()
        await test_delete_operations()
        
        print("\n" + "=" * 50)
        print("✓ ALL CRUD TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
    except Exception as e:
        print(f"✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()
        print("✓ Database connection closed")

if __name__ == "__main__":
    asyncio.run(main())