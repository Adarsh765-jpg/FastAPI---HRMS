/**
 * Navbar Component
 */
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <h1 className="page-title">Welcome, {user?.name}!</h1>
        
        <button onClick={handleLogout} className="btn btn-secondary btn-sm logout-btn">
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
