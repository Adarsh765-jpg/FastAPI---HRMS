/**
 * Dashboard Page - Statistics Overview
 */
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { employeeAPI } from '../api/employeeAPI';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total: 0,
    departments: {},
    loading: true,
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await employeeAPI.getAll({ limit: 100 });
      const employees = response.data.employees;

      // Calculate stats
      const deptCount = {};
      employees.forEach((emp) => {
        deptCount[emp.department] = (deptCount[emp.department] || 0) + 1;
      });

      setStats({
        total: response.data.total,
        departments: deptCount,
        loading: false,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      setStats({ ...stats, loading: false });
    }
  };

  if (stats.loading) {
    return (
      <Layout>
        <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
          <div className="spinner"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="dashboard">
        <h1>Dashboard</h1>
        <p className="subtitle">Welcome to your employee management system</p>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-info">
              <h3>Total Employees</h3>
              <p className="stat-number">{stats.total}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏢</div>
            <div className="stat-info">
              <h3>Departments</h3>
              <p className="stat-number">{Object.keys(stats.departments).length}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">👤</div>
            <div className="stat-info">
              <h3>Your Role</h3>
              <p className="stat-number">{user?.role}</p>
            </div>
          </div>
        </div>

        <div className="card" style={{ marginTop: '32px' }}>
          <h2>Employees by Department</h2>
          <div className="dept-list">
            {Object.entries(stats.departments).map(([dept, count]) => (
              <div key={dept} className="dept-item">
                <span className="dept-name">{dept}</span>
                <span className="dept-count">{count} employees</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
