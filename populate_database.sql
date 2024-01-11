-- Inserir usuários
INSERT INTO users(password, is_active, email)
VALUES 
('$2b$12$1L1QI/yEfn6DFEl.gsFmCOO4E5o6mXQpWh1o0VZpaC.Rbflywk606', true, 'admin@mail.com'),
('$2b$12$1L1QI/yEfn6DFEl.gsFmCOO4E5o6mXQpWh1o0VZpaC.Rbflywk606', true, 'user@mail.com');

-- Inserir rotas
INSERT INTO routes(path, needs_permission)
VALUES
('/auth', false),
('/users', true),
('/permissions', true),
('/permissions-group', true),
('/routes', true),
('/users-and-groups', true),
('/permissions-and-groups', true);

-- Inserir permissões para cada rota
INSERT INTO permissions(route_id, action)
VALUES
-- Rota '/users'
(2, 'create'), (2, 'view'), (2, 'update'), (2, 'delete'),

-- Rota '/permissions'
(3, 'create'), (3, 'view'), (3, 'update'), (3, 'delete'),

-- Rota '/permissions-group'
(4, 'create'), (4, 'view'), (4, 'update'), (4, 'delete'),

-- Rota '/routes'
(5, 'create'), (5, 'view'), (5, 'update'), (5, 'delete'),

-- Rota '/users-and-groups'
(6, 'create'), (6, 'view'), (6, 'update'), (6, 'delete'),

-- Rota '/permissions-and-groups'
(7, 'create'), (7, 'view'), (7, 'update'), (7, 'delete');

-- Inserir grupos de permissões
INSERT INTO permissions_groups(name)
VALUES
-- Criação dos grupos admin e custom user
('admin'), ('custom');

-- Associar cada usuário ao seu respectivo grupo
INSERT INTO permissions_group_user_association(user_id, permission_group_id)
VALUES
(1, 1), (2, 2);

-- Associar todas as permissões ao grupo admin
INSERT INTO permission_association(permission_id, permission_group_id)
SELECT id, 1 FROM permissions;

-- Associar apenas a permissão de 'view' de usuários ao grupo custom user
INSERT INTO permission_association(permission_id, permission_group_id)
SELECT id, 2 FROM permissions WHERE action = 'view' AND route_id = 2;