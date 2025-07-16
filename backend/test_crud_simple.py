#!/usr/bin/env python3
"""
Simple CRUD operations test for Plant Health Monitoring API
"""
import asyncio
from app.core.database import init_db, close_db
from app.services.user_service import UserService
from app.services.plant_service import PlantService
from app.services.diagnosis_service import DiagnosisService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.plant import PlantCreate, PlantUpdate
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate

async def test_all_crud():
    """Test all CRUD operations"""
    try:
        print("=== TESTING ALL CRUD OPERATIONS ===")
        
        # Initialize database
        await init_db()
        print("Database initialized")
        
        # === USER CRUD ===
        print("\n1. TESTING USER CRUD:")
        
        # Create user
        user_data = UserCreate(email="test@example.com", name="Test User")
        user = await UserService.create_user(user_data)
        print(f"  Created user: {user.name} (ID: {user.id})")
        
        # Read user
        retrieved_user = await UserService.get_user_by_id(user.id)
        print(f"  Retrieved user: {retrieved_user.name}")
        
        # Update user
        update_data = UserUpdate(name="Updated Test User")
        updated_user = await UserService.update_user(user.id, update_data)
        print(f"  Updated user: {updated_user.name}")
        
        # === PLANT CRUD ===
        print("\n2. TESTING PLANT CRUD:")
        
        # Create plant
        plant_data = PlantCreate(
            name="Test Plant",
            species="Test Species",
            description="A test plant",
            user_id=user.id
        )
        plant = await PlantService.create_plant(plant_data)
        print(f"  Created plant: {plant.name} (ID: {plant.id})")
        
        # Read plant
        retrieved_plant = await PlantService.get_plant_by_id(plant.id)
        print(f"  Retrieved plant: {retrieved_plant.name}")
        
        # Update plant
        plant_update = PlantUpdate(description="Updated test plant")
        updated_plant = await PlantService.update_plant(plant.id, plant_update)
        print(f"  Updated plant: {updated_plant.description}")
        
        # === DIAGNOSIS CRUD ===
        print("\n3. TESTING DIAGNOSIS CRUD:")
        
        # Create diagnosis
        diagnosis_data = DiagnosisCreate(
            plant_id=plant.id,
            disease_name="Test Disease",
            confidence_score=0.95,
            image_path="/test/image.jpg",
            notes="Test diagnosis",
            is_healthy=False
        )
        diagnosis = await DiagnosisService.create_diagnosis(diagnosis_data)
        print(f"  Created diagnosis: {diagnosis.disease_name} (ID: {diagnosis.id})")
        
        # Read diagnosis
        retrieved_diagnosis = await DiagnosisService.get_diagnosis_by_id(diagnosis.id)
        print(f"  Retrieved diagnosis: {retrieved_diagnosis.disease_name}")
        
        # Update diagnosis
        diagnosis_update = DiagnosisUpdate(confidence_score=0.98)
        updated_diagnosis = await DiagnosisService.update_diagnosis(diagnosis.id, diagnosis_update)
        print(f"  Updated diagnosis confidence: {updated_diagnosis.confidence_score}")
        
        # === COUNTS ===
        print("\n4. TESTING COUNTS:")
        user_count = await UserService.get_users_count()
        plant_count = await PlantService.get_plants_count()
        diagnosis_count = await DiagnosisService.get_diagnoses_count()
        print(f"  Users: {user_count}, Plants: {plant_count}, Diagnoses: {diagnosis_count}")
        
        # === RELATIONSHIPS ===
        print("\n5. TESTING RELATIONSHIPS:")
        user_plants = await PlantService.get_plants_by_user(user.id)
        plant_diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant.id)
        user_diagnoses = await DiagnosisService.get_diagnoses_by_user(user.id)
        print(f"  User has {len(user_plants)} plants")
        print(f"  Plant has {len(plant_diagnoses)} diagnoses")
        print(f"  User has {len(user_diagnoses)} total diagnoses")
        
        # === DELETE OPERATIONS ===
        print("\n6. TESTING DELETE OPERATIONS:")
        
        # Delete diagnosis
        del_success = await DiagnosisService.delete_diagnosis(diagnosis.id)
        print(f"  Deleted diagnosis: {del_success}")
        
        # Delete plant  
        del_success = await PlantService.delete_plant(plant.id)
        print(f"  Deleted plant: {del_success}")
        
        # Delete user
        del_success = await UserService.delete_user(user.id)
        print(f"  Deleted user: {del_success}")
        
        print("\n=== ALL CRUD TESTS COMPLETED SUCCESSFULLY! ===")
        return True
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await close_db()
        print("Database connection closed")

async def main():
    """Main function"""
    success = await test_all_crud()
    if success:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")

if __name__ == "__main__":
    asyncio.run(main())