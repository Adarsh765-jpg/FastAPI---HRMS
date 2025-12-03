/**
 * Sidebar Component
 */
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const { user, canEdit } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>HRMS</h2>
        <p>Employee Management</p>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className="nav-item">
          <span>📊</span> Dashboard
        </NavLink>

        <NavLink to="/employees" end className="nav-item">
          <span>👥</span> Employees
        </NavLink>

        {canEdit && (
          <NavLink to="/employees/add" className="nav-item">
            <span>➕</span> Add Employee
          </NavLink>
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="user-info">
          <div className="user-avatar">{user?.name?.charAt(0)}</div>
          <div>
            <div className="user-name">{user?.name}</div>
            <div className="user-role">
              <span className={`badge badge-${user?.role}`}>{user?.role}</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
