/**
 * Add/Edit Employee Form Component
 */
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';
import { employeeAPI } from '../api/employeeAPI';
import './EmployeeForm.css';

const EmployeeForm = ({ isEdit = false }) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'employee',
    department: '',
    job_role: '',
    salary: '',
  });

  useEffect(() => {
    if (isEdit && id) {
      fetchEmployee();
    }
  }, [id, isEdit]);

  const fetchEmployee = async () => {
    try {
      const response = await employeeAPI.getById(id);
      setFormData(response.data);
    } catch (error) {
      setError('Failed to load employee');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = {
        ...formData,
        salary: parseFloat(formData.salary),
      };

      if (isEdit) {
        await employeeAPI.update(id, data);
      } else {
        await employeeAPI.create(data);
      }

      navigate('/employees');
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to save employee');
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Layout>
      <div className="employee-form-page">
        <h1>{isEdit ? 'Edit Employee' : 'Add New Employee'}</h1>
        <p className="subtitle">
          {isEdit ? 'Update employee information' : 'Fill in the details below'}
        </p>

        <div className="card" style={{ maxWidth: '600px' }}>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">Full Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  disabled={loading}
                />
              </div>
              
              {!isEdit && (
                <div className="form-group">
                  <label htmlFor="role">System Role *</label>
                  <select
                    id="role"
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    required
                    disabled={loading || user?.role === 'hr'}
                  >
                    <option value="employee">Employee</option>
                    {user?.role === 'admin' && (
                      <>
                        <option value="hr">HR Manager</option>
                        <option value="admin">Administrator</option>
                      </>
                    )}
                  </select>
                  {user?.role === 'hr' && <small className="hint">HR can only create Employees</small>}
                </div>
              )}
            </div>

            {!isEdit && (
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="email">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    disabled={loading}
                    placeholder="john@example.com"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password">Password *</label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    disabled={loading}
                    placeholder="Min. 6 characters"
                  />
                </div>
              </div>
            )}

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="department">Department *</label>
                <select
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleChange}
                  required
                  disabled={loading}
                >
                  <option value="">Select Department</option>
                  <option value="Engineering">Engineering</option>
                  <option value="HR">HR</option>
                  <option value="Finance">Finance</option>
                  <option value="Sales">Sales</option>
                  <option value="Marketing">Marketing</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="job_role">Job Role *</label>
                <input
                  type="text"
                  id="job_role"
                  name="job_role"
                  value={formData.job_role}
                  onChange={handleChange}
                  placeholder="e.g., Software Engineer"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="salary">Salary *</label>
                <input
                  type="number"
                  id="salary"
                  name="salary"
                  value={formData.salary}
                  onChange={handleChange}
                  placeholder="e.g., 75000"
                  step="0.01"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Saving...' : isEdit ? 'Update Employee' : 'Add Employee'}
              </button>
              <button
                type="button"
                onClick={() => navigate('/employees')}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
};

export default EmployeeForm;
