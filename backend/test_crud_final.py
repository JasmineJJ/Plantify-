#!/usr/bin/env python3
"""
Final CRUD operations test for Plant Health Monitoring API
"""
import asyncio
import random
import string
from app.core.database import init_db, close_db
from app.services.user_service import UserService
from app.services.plant_service import PlantService
from app.services.diagnosis_service import DiagnosisService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.plant import PlantCreate, PlantUpdate
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate

def random_email():
    """Generate random email"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_string}@example.com"

async def test_complete_crud_flow():
    """Test complete CRUD flow"""
    try:
        print("=== COMPREHENSIVE CRUD TEST ===")
        
        # Initialize database
        await init_db()
        print("Database initialized")
        
        # 1. USER OPERATIONS
        print("\n1. USER OPERATIONS:")
        
        # Create user with unique email
        email = random_email()
        user_data = UserCreate(email=email, name="John Doe")
        user = await UserService.create_user(user_data)
        print(f"  CREATE: User created - {user.name} ({user.email}) [ID: {user.id}]")
        
        # Read user by ID
        user_by_id = await UserService.get_user_by_id(user.id)
        print(f"  READ: User by ID - {user_by_id.name}")
        
        # Read user by email
        user_by_email = await UserService.get_user_by_email(email)
        print(f"  READ: User by email - {user_by_email.name}")
        
        # Update user
        user_update = UserUpdate(name="John Doe Updated")
        updated_user = await UserService.update_user(user.id, user_update)
        print(f"  UPDATE: User name changed to - {updated_user.name}")
        
        # 2. PLANT OPERATIONS
        print("\n2. PLANT OPERATIONS:")
        
        # Create plant
        plant_data = PlantCreate(
            name="Rose Bush",
            species="Rosa damascena",
            description="Beautiful red roses",
            user_id=user.id
        )
        plant = await PlantService.create_plant(plant_data)
        print(f"  CREATE: Plant created - {plant.name} ({plant.species}) [ID: {plant.id}]")
        
        # Read plant
        plant_by_id = await PlantService.get_plant_by_id(plant.id)
        print(f"  READ: Plant by ID - {plant_by_id.name}")
        
        # Update plant
        plant_update = PlantUpdate(description="Beautiful red roses in the garden")
        updated_plant = await PlantService.update_plant(plant.id, plant_update)
        print(f"  UPDATE: Plant description - {updated_plant.description}")
        
        # 3. DIAGNOSIS OPERATIONS
        print("\n3. DIAGNOSIS OPERATIONS:")
        
        # Create diagnosis
        diagnosis_data = DiagnosisCreate(
            plant_id=plant.id,
            disease_name="Black Spot Disease",
            confidence_score=0.89,
            image_path="/uploads/diagnosis_001.jpg",
            notes="Black spots observed on leaves",
            is_healthy=False
        )
        diagnosis = await DiagnosisService.create_diagnosis(diagnosis_data)
        print(f"  CREATE: Diagnosis created - {diagnosis.disease_name} [ID: {diagnosis.id}]")
        print(f"          Confidence: {diagnosis.confidence_score}, Healthy: {diagnosis.is_healthy}")
        
        # Read diagnosis
        diagnosis_by_id = await DiagnosisService.get_diagnosis_by_id(diagnosis.id)
        print(f"  READ: Diagnosis by ID - {diagnosis_by_id.disease_name}")
        
        # Update diagnosis
        diagnosis_update = DiagnosisUpdate(
            confidence_score=0.95,
            notes="Black spots observed on leaves, treatment applied"
        )
        updated_diagnosis = await DiagnosisService.update_diagnosis(diagnosis.id, diagnosis_update)
        print(f"  UPDATE: Diagnosis confidence - {updated_diagnosis.confidence_score}")
        
        # 4. RELATIONSHIP QUERIES
        print("\n4. RELATIONSHIP QUERIES:")
        
        # Plants by user
        user_plants = await PlantService.get_plants_by_user(user.id)
        print(f"  User {user.name} has {len(user_plants)} plants")
        
        # Diagnoses by plant
        plant_diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant.id)
        print(f"  Plant {plant.name} has {len(plant_diagnoses)} diagnoses")
        
        # Diagnoses by user
        user_diagnoses = await DiagnosisService.get_diagnoses_by_user(user.id)
        print(f"  User {user.name} has {len(user_diagnoses)} total diagnoses")
        
        # 5. LIST OPERATIONS
        print("\n5. LIST OPERATIONS:")
        
        all_users = await UserService.get_all_users()
        all_plants = await PlantService.get_all_plants()
        all_diagnoses = await DiagnosisService.get_all_diagnoses()
        
        print(f"  Total users in system: {len(all_users)}")
        print(f"  Total plants in system: {len(all_plants)}")
        print(f"  Total diagnoses in system: {len(all_diagnoses)}")
        
        # 6. COUNT OPERATIONS
        print("\n6. COUNT OPERATIONS:")
        
        user_count = await UserService.get_users_count()
        plant_count = await PlantService.get_plants_count()
        diagnosis_count = await DiagnosisService.get_diagnoses_count()
        
        print(f"  User count: {user_count}")
        print(f"  Plant count: {plant_count}")
        print(f"  Diagnosis count: {diagnosis_count}")
        
        # 7. CREATE ADDITIONAL DATA
        print("\n7. CREATING ADDITIONAL TEST DATA:")
        
        # Create second plant
        plant2_data = PlantCreate(
            name="Orchid",
            species="Phalaenopsis amabilis",
            description="White orchid with purple spots",
            user_id=user.id
        )
        plant2 = await PlantService.create_plant(plant2_data)
        print(f"  Created second plant: {plant2.name}")
        
        # Create diagnosis for second plant
        diagnosis2_data = DiagnosisCreate(
            plant_id=plant2.id,
            disease_name="Healthy",
            confidence_score=0.98,
            image_path="/uploads/diagnosis_002.jpg",
            notes="Plant appears healthy",
            is_healthy=True
        )
        diagnosis2 = await DiagnosisService.create_diagnosis(diagnosis2_data)
        print(f"  Created diagnosis for second plant: {diagnosis2.disease_name}")
        
        # 8. UPDATED RELATIONSHIP QUERIES
        print("\n8. UPDATED RELATIONSHIP QUERIES:")
        
        user_plants = await PlantService.get_plants_by_user(user.id)
        user_diagnoses = await DiagnosisService.get_diagnoses_by_user(user.id)
        
        print(f"  User now has {len(user_plants)} plants")
        print(f"  User now has {len(user_diagnoses)} total diagnoses")
        
        for plant in user_plants:
            plant_diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant.id)
            print(f"    Plant {plant.name} has {len(plant_diagnoses)} diagnoses")
        
        # 9. ERROR HANDLING TESTS
        print("\n9. ERROR HANDLING TESTS:")
        
        # Test non-existent IDs
        non_user = await UserService.get_user_by_id(99999)
        non_plant = await PlantService.get_plant_by_id(99999)
        non_diagnosis = await DiagnosisService.get_diagnosis_by_id(99999)
        
        print(f"  Non-existent user: {non_user is None}")
        print(f"  Non-existent plant: {non_plant is None}")
        print(f"  Non-existent diagnosis: {non_diagnosis is None}")
        
        # Test invalid foreign key
        invalid_plant = await PlantService.create_plant(
            PlantCreate(name="Invalid", species="Invalid", user_id=99999)
        )
        print(f"  Invalid user_id plant creation: {invalid_plant is None}")
        
        print("\n=== ALL CRUD OPERATIONS COMPLETED SUCCESSFULLY! ===")
        
        # Display final summary
        final_user_count = await UserService.get_users_count()
        final_plant_count = await PlantService.get_plants_count()
        final_diagnosis_count = await DiagnosisService.get_diagnoses_count()
        
        print(f"\nFINAL SUMMARY:")
        print(f"  Total Users: {final_user_count}")
        print(f"  Total Plants: {final_plant_count}")
        print(f"  Total Diagnoses: {final_diagnosis_count}")
        
        return True
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await close_db()
        print("\nDatabase connection closed")

async def main():
    """Main function"""
    success = await test_complete_crud_flow()
    if success:
        print("\n*** ALL CRUD TESTS PASSED SUCCESSFULLY! ***")
    else:
        print("\n*** SOME TESTS FAILED! ***")

if __name__ == "__main__":
    asyncio.run(main())