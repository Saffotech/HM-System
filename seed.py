from database import SessionLocal
from Models.user import User  # ← add this
from Models.role import Role, Permission, RolePermission

db = SessionLocal()

# rest of your seed code stays the same...
permissions = [
    "patients:view", "patients:create", "patients:update", "patients:delete",
    "users:list", "users:create", "users:delete", "users:activate",
    "roles:create", "roles:view",
    "billing:view", "billing:create",
    "lab:view", "lab:create",
    "prescriptions:create",
    "appointments:view", "appointments:create", "appointments:update",
    "reports:view", "settings:manage"
]

perm_objects = {}
for p in permissions:
    perm = Permission(name=p)
    db.add(perm)
    db.flush()
    perm_objects[p] = perm.id

# create roles
roles_data = {
    "admin":        list(perm_objects.keys()),
    "doctor":       ["patients:view","patients:create","patients:update",
                     "prescriptions:create","lab:view","lab:create","appointments:view"],
    "nurse":        ["patients:view","vitals:create","appointments:view","lab:view"],
    "receptionist": ["patients:view","patients:create","appointments:create",
                     "appointments:update","billing:view"],
    "pharmacist":   ["prescriptions:create","patients:view"]
}

for role_name, role_perms in roles_data.items():
    role = Role(name=role_name)
    db.add(role)
    db.flush()
    for perm_name in role_perms:
        if perm_name in perm_objects:
            db.add(RolePermission(role_id=role.id, permission_id=perm_objects[perm_name]))

db.commit()
print("Roles and permissions seeded!")
db.close()