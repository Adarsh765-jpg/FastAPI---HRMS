/**
 * Employees List Page with Filtering and Pagination
 */
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import { employeeAPI } from '../api/employeeAPI';
import { useAuth } from '../context/AuthContext';
import './Employees.css';

const Employees = () => {
  const { canEdit, role } = useAuth();
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    total_pages: 0,
  });
  const [filters, setFilters] = useState({
    search: '',
    department: '',
  });

  useEffect(() => {
    fetchEmployees();
  }, [pagination.page, filters]);

  const fetchEmployees = async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...(filters.search && { search: filters.search }),
        ...(filters.department && { department: filters.department }),
      };

      const response = await employeeAPI.getAll(params);
      setEmployees(response.data.employees);
      setPagination({
        ...pagination,
        total: response.data.total,
        total_pages: response.data.total_pages,
      });
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
    setLoading(false);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPagination({ ...pagination, page: 1 });
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Delete employee ${name}?`)) return;

    try {
      await employeeAPI.delete(id);
      fetchEmployees();
    } catch (error) {
      alert('Failed to delete employee');
    }
  };

  return (
    <Layout>
      <div className="employees-page">
        <div className="page-header">
          <div>
            <h1>Employees</h1>
            <p className="subtitle">Manage all employee records</p>
          </div>
          {canEdit && (
            <Link to="/employees/add" className="btn btn-primary">
              ➕ Add Employee
            </Link>
          )}
        </div>

        <div className="card">
          <form onSubmit={handleSearch} className="filters">
            <input
              type="text"
              placeholder="Search by name..."
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              className="search-input"
            />
            <select
              value={filters.department}
              onChange={(e) => {
                setFilters({ ...filters, department: e.target.value });
                setPagination({ ...pagination, page: 1 });
              }}
            >
              <option value="">All Departments</option>
              <option value="Engineering">Engineering</option>
              <option value="HR">HR</option>
              <option value="Finance">Finance</option>
              <option value="Sales">Sales</option>
              <option value="Marketing">Marketing</option>
            </select>
            <button type="submit" className="btn btn-primary">
              Search
            </button>
            {(filters.search || filters.department) && (
              <button
                type="button"
                onClick={() => {
                  setFilters({ search: '', department: '' });
                  setPagination({ ...pagination, page: 1 });
                }}
                className="btn btn-secondary"
              >
                Clear
              </button>
            )}
          </form>

          {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
              <div className="spinner"></div>
            </div>
          ) : employees.length === 0 ? (
            <div className="empty-state">
              <p>No employees found</p>
            </div>
          ) : (
            <>
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Department</th>
                      <th>Job Role</th>
                      {role !== 'employee' && <th>Salary</th>}
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {employees.map((emp) => (
                      <tr key={emp.id}>
                        <td>{emp.name}</td>
                        <td>{emp.department}</td>
                        <td>{emp.job_role}</td>
                        {role !== 'employee' && (
                          <td>${emp.salary?.toLocaleString() || 'N/A'}</td>
                        )}
                        <td>
                          <div className="actions">
                            <Link to={`/employees/${emp.id}`} className="btn btn-sm btn-secondary">
                              View
                            </Link>
                            {canEdit && (
                              <>
                                <Link to={`/employees/edit/${emp.id}`} className="btn btn-sm btn-primary">
                                  Edit
                                </Link>
                                <button
                                  onClick={() => handleDelete(emp.id, emp.name)}
                                  className="btn btn-sm btn-danger"
                                >
                                  Delete
                                </button>
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {pagination.total_pages > 1 && (
                <div className="pagination">
                  <button
                    onClick={() => setPagination({ ...pagination, page: pagination.page - 1 })}
                    disabled={pagination.page === 1}
                    className="btn btn-secondary btn-sm"
                  >
                    Previous
                  </button>
                  <span className="page-info">
                    Page {pagination.page} of {pagination.total_pages} ({pagination.total} total)
                  </span>
                  <button
                    onClick={() => setPagination({ ...pagination, page: pagination.page + 1 })}
                    disabled={pagination.page >= pagination.total_pages}
                    className="btn btn-secondary btn-sm"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Employees;
