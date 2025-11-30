/**
 * View Employee Details Page
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Layout from '../components/Layout';
import { employeeAPI } from '../api/employeeAPI';
import { useAuth } from '../context/AuthContext';
import './EmployeeDetail.css';

const EmployeeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { canEdit, role } = useAuth();
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployee();
  }, [id]);

  const fetchEmployee = async () => {
    try {
      const response = await employeeAPI.getById(id);
      setEmployee(response.data);
    } catch (error) {
      alert('Employee not found');
      navigate('/employees');
    }
    setLoading(false);
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete employee ${employee.name}?`)) return;

    try {
      await employeeAPI.delete(id);
      navigate('/employees');
    } catch (error) {
      alert('Failed to delete employee');
    }
  };

  if (loading) {
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
      <div className="employee-detail-page">
        <div className="page-header">
          <div>
            <h1>{employee.name}</h1>
            <p className="subtitle">Employee Details</p>
          </div>
          <div className="actions">
            {canEdit && (
              <>
                <Link to={`/employees/edit/${id}`} className="btn btn-primary">
                  Edit
                </Link>
                <button onClick={handleDelete} className="btn btn-danger">
                  Delete
                </button>
              </>
            )}
          </div>
        </div>

        <div className="card">
          <div className="detail-grid">
            <div className="detail-item">
              <label>Full Name</label>
              <p>{employee.name}</p>
            </div>

            <div className="detail-item">
              <label>Department</label>
              <p>{employee.department}</p>
            </div>

            <div className="detail-item">
              <label>Job Role</label>
              <p>{employee.job_role}</p>
            </div>

            {role !== 'employee' && employee.salary !== undefined && (
              <div className="detail-item">
                <label>Salary</label>
                <p className="salary">${employee.salary?.toLocaleString()}</p>
              </div>
            )}

            {employee.created_at && (
              <div className="detail-item">
                <label>Created At</label>
                <p>{new Date(employee.created_at).toLocaleDateString()}</p>
              </div>
            )}
          </div>
        </div>

        <Link to="/employees" className="btn btn-secondary" style={{ marginTop: '20px' }}>
          ← Back to Employees
        </Link>
      </div>
    </Layout>
  );
};

export default EmployeeDetail;
