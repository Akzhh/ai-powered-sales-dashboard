import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { getStats, getSales, getModelInfo, trainModel, getTrainStatus } from '../api';
import { useToast } from '../components/Toast';
import StatCard from '../components/StatCard';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DashboardPage() {
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [stats, setStats] = useState({ total_sales: 0, total_profit: 0, total_orders: 0 });
  const [sales, setSales] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [trainState, setTrainState] = useState({ status: 'completed', progress: 0 });
  const [trainingLoading, setTrainingLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, salesRes, infoRes, statusRes] = await Promise.all([
        getStats(),
        getSales(),
        getModelInfo(),
        getTrainStatus()
      ]);

      if (statsRes.ok) setStats(statsRes.data);
      else showToast('Failed to load dashboard metrics', 'error');

      if (salesRes.ok) setSales(salesRes.data);
      else showToast('Failed to load sales records', 'error');

      if (infoRes.ok) setModelInfo(infoRes.data);
      if (statusRes.ok) setTrainState(statusRes.data);
    } catch {
      showToast('Connection error loading dashboard', 'error');
    }
  };

  // Poll training status if background trainer is running
  useEffect(() => {
    let interval = null;
    if (trainState.status === 'training') {
      interval = setInterval(async () => {
        try {
          const statusRes = await getTrainStatus();
          if (statusRes.ok) {
            setTrainState(statusRes.data);
            if (statusRes.data.status !== 'training') {
              clearInterval(interval);
              // Refresh model details
              const infoRes = await getModelInfo();
              if (infoRes.ok) setModelInfo(infoRes.data);
              
              if (statusRes.data.status === 'completed') {
                showToast('AI Model training completed successfully!', 'success');
              } else if (statusRes.data.status === 'failed') {
                showToast('AI Model training failed.', 'error');
              }
            }
          }
        } catch {
          // Silent catch to prevent error logs on connection issues
        }
      }, 2000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [trainState.status]);

  const handleRetrain = async () => {
    setTrainingLoading(true);
    try {
      const res = await trainModel();
      if (res.ok) {
        showToast(res.data.message || 'Model training started.', 'success');
        setTrainState({ status: 'training', progress: 0 });
      } else {
        showToast(res.data?.error || 'Failed to start training', 'error');
      }
    } catch {
      showToast('Error initiating model training', 'error');
    } finally {
      setTrainingLoading(false);
    }
  };

  // Build doughnut chart data from sales by category
  const categoryTotals = {};
  sales.forEach((s) => {
    categoryTotals[s.category] = (categoryTotals[s.category] || 0) + s.total;
  });

  const chartColors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4'];

  const chartData = {
    labels: Object.keys(categoryTotals),
    datasets: [
      {
        data: Object.values(categoryTotals),
        backgroundColor: chartColors.slice(0, Object.keys(categoryTotals).length),
        borderWidth: 2,
        borderColor: '#101626',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#94A3B8',
          font: { family: 'Outfit', size: 12 },
        },
      },
    },
  };

  const latestSales = [...sales].reverse().slice(0, 5);

  const formatCurrency = (val) =>
    `₹ ${val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  return (
    <div className="content-section">
      {/* Stats Cards */}
      <div className="stats-grid">
        <StatCard
          title="Total Sales"
          value={formatCurrency(stats.total_sales)}
          icon="fa-indian-rupee-sign"
          colorClass="blue"
        />
        <StatCard
          title="Total Profit"
          value={formatCurrency(stats.total_profit)}
          icon="fa-wallet"
          colorClass="green"
        />
        <StatCard
          title="Total Orders"
          value={stats.total_orders}
          icon="fa-shopping-bag"
          colorClass="orange"
        />
      </div>

      {/* AI Model Status Card */}
      <div className="glass-card ai-model-card" style={{ marginBottom: '24px' }}>
        <div className="card-header" style={{ marginBottom: '16px' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <i className="fa-solid fa-brain" style={{ color: 'var(--accent-purple)' }} />
            AI Sales Forecasting Model
          </h3>
          <span className={`badge ${trainState.status === 'training' ? 'badge-purple' : ''}`}>
            {trainState.status.toUpperCase()}
          </span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px', alignItems: 'center' }}>
          <div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '4px' }}>Algorithm</p>
            <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'white' }}>{modelInfo?.algorithm || 'Linear Regression'}</h4>
          </div>
          <div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '4px' }}>Model Accuracy (R²)</p>
            <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--accent-blue)' }}>
              {modelInfo?.accuracy ? `${(modelInfo.accuracy * 100).toFixed(2)}%` : 'N/A'}
            </h4>
          </div>
          <div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '4px' }}>Dataset Size</p>
            <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'white' }}>{modelInfo?.dataset_size ? `${modelInfo.dataset_size} rows` : '0 rows'}</h4>
          </div>
          <div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '4px' }}>Last Trained</p>
            <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'white' }}>{modelInfo?.training_date || 'N/A'}</h4>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {trainState.status === 'training' ? (
              <div style={{ width: '100%' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                  <span>Training Progress</span>
                  <span>{trainState.progress}%</span>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${trainState.progress}%`, height: '100%', background: 'var(--accent-purple)', transition: 'width 0.3s ease' }} />
                </div>
              </div>
            ) : (
              <button
                className="btn-upload"
                onClick={handleRetrain}
                disabled={trainingLoading || trainState.status === 'training'}
                style={{ alignSelf: 'flex-start', width: '100%', justifyContent: 'center' }}
                id="btn-retrain-model"
              >
                <i className="fa-solid fa-sync fa-spin" style={{ display: trainingLoading ? 'inline-block' : 'none', marginRight: '6px' }} />
                <i className="fa-solid fa-bolt" style={{ display: trainingLoading ? 'none' : 'inline-block' }} />
                Retrain Model
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Dashboard Grid */}
      <div className="dashboard-grid">
        {/* Chart Card */}
        <div className="glass-card main-chart-preview">
          <div className="card-header">
            <h3>Sales Distribution</h3>
            <span className="badge">Live Preview</span>
          </div>
          <div className="canvas-container">
            {Object.keys(categoryTotals).length > 0 ? (
              <Doughnut data={chartData} options={chartOptions} />
            ) : (
              <div className="empty-state">No sales data to display</div>
            )}
          </div>
        </div>

        {/* Recent Orders */}
        <div className="glass-card latest-sales-preview">
          <div className="card-header">
            <h3>Recent Orders</h3>
            <button
              className="btn-text-action"
              onClick={() => navigate('/sales')}
              id="btn-view-all-sales"
            >
              View All
            </button>
          </div>
          <div className="recent-list-container">
            <table className="data-table-minimal">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {latestSales.length === 0 ? (
                  <tr>
                    <td colSpan="4" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                      No sales recorded yet.
                    </td>
                  </tr>
                ) : (
                  latestSales.map((s) => (
                    <tr key={s.id}>
                      <td>{s.date}</td>
                      <td style={{ fontWeight: 500, color: 'white' }}>{s.product}</td>
                      <td><span className="badge">{s.category}</span></td>
                      <td style={{ fontWeight: 600, color: 'var(--accent-blue)' }}>
                        ₹ {s.total.toFixed(2)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
