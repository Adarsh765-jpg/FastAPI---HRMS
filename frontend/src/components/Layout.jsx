/**
 * Layout wrapper for authenticated pages
 */
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <Sidebar />
      <div className="main-wrapper">
        <Navbar />
        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
