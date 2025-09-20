import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Icons
import { 
  Shield, 
  Search, 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  Server, 
  FileText, 
  Settings, 
  Upload,
  Play,
  CheckCircle,
  XCircle,
  Clock,
  Eye,
  Download,
  BarChart3,
  Home,
  Target,
  Zap,
  Activity,
  Database,
  Bell,
  Filter
} from 'lucide-react';

// UI Components
import { Button } from './components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Textarea } from './components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Alert, AlertDescription, AlertTitle } from './components/ui/alert';
import { Progress } from './components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';

// Charts
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

// Dropzone
import { useDropzone } from 'react-dropzone';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Constants
const SEVERITY_COLORS = {
  critical: '#dc2626',
  high: '#ea580c',
  medium: '#ca8a04',
  low: '#16a34a',
  info: '#2563eb'
};

const SEVERITY_BADGES = {
  critical: 'destructive',
  high: 'destructive',
  medium: 'default',
  low: 'secondary',
  info: 'outline'
};

// Navigation Component
const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/assets', icon: Server, label: 'Assets' },
    { path: '/findings', icon: AlertTriangle, label: 'Findings' },
    { path: '/scans', icon: Search, label: 'Scans' },
    { path: '/reports', icon: BarChart3, label: 'Reports' }
  ];

  return (
    <nav className="bg-slate-900 text-white w-64 min-h-screen fixed left-0 top-0 z-40">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-red-600 p-2 rounded-lg">
            <Shield className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold">VulnGuard</h1>
            <p className="text-sm text-slate-400">Security Platform</p>
          </div>
        </div>
        
        <div className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive 
                    ? 'bg-red-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="h-5 w-5" />
                {item.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

// Dashboard Component
const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600"></div>
      </div>
    );
  }

  const severityData = stats?.severity_breakdown ? Object.entries(stats.severity_breakdown).map(([key, value]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value,
    color: SEVERITY_COLORS[key]
  })) : [];

  const trendData = [
    { month: 'Jan', findings: 45, resolved: 32 },
    { month: 'Feb', findings: 52, resolved: 28 },
    { month: 'Mar', findings: 61, resolved: 45 },
    { month: 'Apr', findings: 38, resolved: 52 },
    { month: 'May', findings: 73, resolved: 41 },
    { month: 'Jun', findings: 42, resolved: 65 }
  ];

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-8 text-white overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Vulnerability Management Dashboard</h1>
              <p className="text-slate-300 text-lg">
                Comprehensive security posture overview and threat analysis
              </p>
            </div>
            <div className="hidden md:block">
              <img 
                src="https://images.unsplash.com/photo-1708807472445-d33589e6b090?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMG1vbml0b3Jpbmd8ZW58MHx8fHwxNzU4MzMzOTk5fDA&ixlib=rb-4.1.0&q=85"
                alt="Security Operations Center"
                className="w-64 h-40 object-cover rounded-lg opacity-80"
              />
            </div>
          </div>
        </div>
        <div className="absolute inset-0 bg-gradient-to-r from-red-600/20 to-orange-600/10"></div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-l-4 border-l-red-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_assets || 0}</div>
            <p className="text-xs text-muted-foreground">+12% from last month</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-orange-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Findings</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_findings || 0}</div>
            <p className="text-xs text-muted-foreground">-8% from last week</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-yellow-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Issues</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {stats?.severity_breakdown?.critical || 0}
            </div>
            <p className="text-xs text-muted-foreground">Requires immediate attention</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Resolved This Week</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">47</div>
            <p className="text-xs text-muted-foreground">+23% increase</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Vulnerability Trends</CardTitle>
            <CardDescription>Monthly findings and resolution rates</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="findings" stackId="1" stroke="#dc2626" fill="#dc2626" fillOpacity={0.6} />
                <Area type="monotone" dataKey="resolved" stackId="2" stroke="#16a34a" fill="#16a34a" fillOpacity={0.6} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Severity Distribution</CardTitle>
            <CardDescription>Current vulnerability breakdown by severity</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Scans</CardTitle>
            <CardDescription>Latest vulnerability scans performed</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.recent_scans?.slice(0, 5).map((scan) => (
                <div key={scan.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-full ${
                      scan.status === 'completed' ? 'bg-green-100 text-green-600' :
                      scan.status === 'running' ? 'bg-blue-100 text-blue-600' :
                      'bg-red-100 text-red-600'
                    }`}>
                      {scan.status === 'completed' ? <CheckCircle className="h-4 w-4" /> :
                       scan.status === 'running' ? <Activity className="h-4 w-4" /> :
                       <XCircle className="h-4 w-4" />}
                    </div>
                    <div>
                      <p className="font-medium">{scan.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {scan.findings_count} findings • {scan.scan_type}
                      </p>
                    </div>
                  </div>
                  <Badge variant={scan.status === 'completed' ? 'default' : 'secondary'}>
                    {scan.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top CVEs</CardTitle>
            <CardDescription>Most frequently detected vulnerabilities</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.top_cves?.slice(0, 5).map((cve, index) => (
                <div key={cve._id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="bg-red-100 text-red-600 p-2 rounded-full text-sm font-bold">
                      #{index + 1}
                    </div>
                    <div>
                      <p className="font-medium">{cve._id}</p>
                      <p className="text-sm text-muted-foreground">
                        {cve.count} occurrences
                      </p>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Assets Component
const Assets = () => {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [newAsset, setNewAsset] = useState({
    hostname: '',
    ip_address: '',
    asset_type: 'server',
    owner: '',
    environment: 'production',
    criticality: 3
  });

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${API}/assets`);
      setAssets(response.data);
    } catch (error) {
      console.error('Failed to fetch assets:', error);
      toast.error('Failed to load assets');
    } finally {
      setLoading(false);
    }
  };

  const handleAddAsset = async () => {
    try {
      await axios.post(`${API}/assets`, newAsset);
      toast.success('Asset added successfully');
      setShowAddDialog(false);
      setNewAsset({
        hostname: '',
        ip_address: '',
        asset_type: 'server',
        owner: '',
        environment: 'production',
        criticality: 3
      });
      fetchAssets();
    } catch (error) {
      console.error('Failed to add asset:', error);
      toast.error('Failed to add asset');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Asset Management</h1>
          <p className="text-muted-foreground">Manage and monitor your infrastructure assets</p>
        </div>
        <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
          <DialogTrigger asChild>
            <Button>
              <Target className="h-4 w-4 mr-2" />
              Add Asset
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Asset</DialogTitle>
              <DialogDescription>
                Register a new asset for vulnerability monitoring
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="hostname">Hostname</Label>
                <Input
                  id="hostname"
                  value={newAsset.hostname}
                  onChange={(e) => setNewAsset({...newAsset, hostname: e.target.value})}
                  placeholder="web-server-01"
                />
              </div>
              <div>
                <Label htmlFor="ip_address">IP Address</Label>
                <Input
                  id="ip_address"
                  value={newAsset.ip_address}
                  onChange={(e) => setNewAsset({...newAsset, ip_address: e.target.value})}
                  placeholder="192.168.1.100"
                />
              </div>
              <div>
                <Label htmlFor="asset_type">Asset Type</Label>
                <Select value={newAsset.asset_type} onValueChange={(value) => setNewAsset({...newAsset, asset_type: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select asset type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="server">Server</SelectItem>
                    <SelectItem value="workstation">Workstation</SelectItem>
                    <SelectItem value="network_device">Network Device</SelectItem>
                    <SelectItem value="database">Database</SelectItem>
                    <SelectItem value="web_application">Web Application</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="owner">Owner</Label>
                <Input
                  id="owner"
                  value={newAsset.owner}
                  onChange={(e) => setNewAsset({...newAsset, owner: e.target.value})}
                  placeholder="IT Team"
                />
              </div>
              <div>
                <Label htmlFor="environment">Environment</Label>
                <Select value={newAsset.environment} onValueChange={(value) => setNewAsset({...newAsset, environment: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select environment" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="production">Production</SelectItem>
                    <SelectItem value="staging">Staging</SelectItem>
                    <SelectItem value="development">Development</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="criticality">Criticality (1-5)</Label>
                <Select value={newAsset.criticality.toString()} onValueChange={(value) => setNewAsset({...newAsset, criticality: parseInt(value)})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select criticality" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 - Critical</SelectItem>
                    <SelectItem value="2">2 - High</SelectItem>
                    <SelectItem value="3">3 - Medium</SelectItem>
                    <SelectItem value="4">4 - Low</SelectItem>
                    <SelectItem value="5">5 - Minimal</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleAddAsset} className="w-full">
                Add Asset
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {assets.map((asset) => (
          <Card key={asset.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{asset.hostname}</CardTitle>
                <Badge variant={asset.environment === 'production' ? 'destructive' : 'secondary'}>
                  {asset.environment}
                </Badge>
              </div>
              <CardDescription>{asset.ip_address}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Type:</span>
                <span className="capitalize">{asset.asset_type.replace('_', ' ')}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Owner:</span>
                <span>{asset.owner || 'Unassigned'}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Criticality:</span>
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className={`w-2 h-2 rounded-full ${
                        i < (6 - asset.criticality) ? 'bg-red-500' : 'bg-gray-200'
                      }`}
                    />
                  ))}
                </div>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Last Scan:</span>
                <span>{asset.last_scan ? new Date(asset.last_scan).toLocaleDateString() : 'Never'}</span>
              </div>
              <div className="flex gap-2 pt-2">
                <Button variant="outline" size="sm" className="flex-1">
                  <Eye className="h-4 w-4 mr-2" />
                  View
                </Button>
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

// File Upload Component
const FileUploadCard = ({ onFileUpload }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: onFileUpload,
    accept: {
      'application/json': ['.json'],
      'text/xml': ['.xml'],
      'text/csv': ['.csv'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Scan Results</CardTitle>
        <CardDescription>
          Upload vulnerability scan files (JSON, XML, CSV formats supported)
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          {isDragActive ? (
            <p className="text-blue-600">Drop the file here...</p>
          ) : (
            <div>
              <p className="mb-2">Drag & drop a scan file here, or click to select</p>
              <p className="text-sm text-muted-foreground">
                Supports: Nessus, OpenVAS, Nmap, custom JSON/CSV formats
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Scans Component
const Scans = () => {
  const [scans, setScans] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewScan, setShowNewScan] = useState(false);
  const [newScan, setNewScan] = useState({
    name: '',
    targets: '',
    scan_type: 'network'
  });

  useEffect(() => {
    fetchScans();
    fetchAssets();
  }, []);

  const fetchScans = async () => {
    try {
      // Mock data for demo
      setScans([
        {
          id: '1',
          name: 'Weekly Network Scan',
          scan_type: 'network',
          status: 'completed',
          findings_count: 23,
          started_at: new Date().toISOString(),
          completed_at: new Date().toISOString()
        },
        {
          id: '2',
          name: 'Production Servers',
          scan_type: 'host',
          status: 'running',
          findings_count: 0,
          started_at: new Date().toISOString()
        }
      ]);
    } catch (error) {
      console.error('Failed to fetch scans:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${API}/assets`);
      setAssets(response.data);
    } catch (error) {
      console.error('Failed to fetch assets:', error);
    }
  };

  const handleFileUpload = async (acceptedFiles, assetId) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('scan_name', `File Upload - ${file.name}`);
    formData.append('asset_id', assetId);

    try {
      const response = await axios.post(`${API}/scan/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      toast.success(`Successfully processed ${response.data.findings_count} findings`);
      fetchScans();
    } catch (error) {
      console.error('File upload failed:', error);
      toast.error('Failed to upload scan file');
    }
  };

  const handleNetworkScan = async () => {
    try {
      const targets = newScan.targets.split(',').map(t => t.trim());
      const response = await axios.post(`${API}/scan/network`, {
        targets,
        scan_name: newScan.name
      });
      
      toast.success(`Network scan initiated: ${response.data.findings_count} findings discovered`);
      setShowNewScan(false);
      fetchScans();
    } catch (error) {
      console.error('Network scan failed:', error);
      toast.error('Failed to start network scan');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Vulnerability Scans</h1>
          <p className="text-muted-foreground">Initiate and manage security scans</p>
        </div>
        <Dialog open={showNewScan} onOpenChange={setShowNewScan}>
          <DialogTrigger asChild>
            <Button>
              <Play className="h-4 w-4 mr-2" />
              New Scan
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Start New Scan</DialogTitle>
              <DialogDescription>
                Configure and launch a vulnerability scan
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="scan_name">Scan Name</Label>
                <Input
                  id="scan_name"
                  value={newScan.name}
                  onChange={(e) => setNewScan({...newScan, name: e.target.value})}
                  placeholder="Production Network Scan"
                />
              </div>
              <div>
                <Label htmlFor="targets">Targets</Label>
                <Textarea
                  id="targets"
                  value={newScan.targets}
                  onChange={(e) => setNewScan({...newScan, targets: e.target.value})}
                  placeholder="192.168.1.0/24, example.com, 10.0.0.1-10.0.0.50"
                  rows={3}
                />
              </div>
              <Button onClick={handleNetworkScan} className="w-full">
                Start Scan
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <Tabs defaultValue="upload" className="space-y-6">
        <TabsList>
          <TabsTrigger value="upload">File Upload</TabsTrigger>
          <TabsTrigger value="history">Scan History</TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <FileUploadCard 
              onFileUpload={(files) => {
                if (assets.length > 0) {
                  handleFileUpload(files, assets[0].id);
                } else {
                  toast.error('Please add an asset first');
                }
              }} 
            />
            
            <Card>
              <CardHeader>
                <CardTitle>Supported Formats</CardTitle>
                <CardDescription>Upload scan results from various security tools</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="font-medium">Nessus (.nessus)</p>
                    <p className="text-sm text-muted-foreground">Tenable Nessus scan results</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="font-medium">OpenVAS (.xml)</p>
                    <p className="text-sm text-muted-foreground">OpenVAS XML reports</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="font-medium">Custom JSON/CSV</p>
                    <p className="text-sm text-muted-foreground">Structured vulnerability data</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="history" className="space-y-6">
          <div className="space-y-4">
            {scans.map((scan) => (
              <Card key={scan.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-full ${
                        scan.status === 'completed' ? 'bg-green-100 text-green-600' :
                        scan.status === 'running' ? 'bg-blue-100 text-blue-600' :
                        'bg-red-100 text-red-600'
                      }`}>
                        {scan.status === 'completed' ? <CheckCircle className="h-6 w-6" /> :
                         scan.status === 'running' ? <Activity className="h-6 w-6 animate-pulse" /> :
                         <XCircle className="h-6 w-6" />}
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">{scan.name}</h3>
                        <p className="text-muted-foreground">
                          {scan.scan_type} scan • {scan.findings_count} findings
                        </p>
                        <p className="text-sm text-muted-foreground">
                          Started: {new Date(scan.started_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={
                        scan.status === 'completed' ? 'default' :
                        scan.status === 'running' ? 'secondary' : 'destructive'
                      }>
                        {scan.status}
                      </Badge>
                      <Button variant="outline" size="sm">
                        <Eye className="h-4 w-4 mr-2" />
                        View Results
                      </Button>
                    </div>
                  </div>
                  {scan.status === 'running' && (
                    <div className="mt-4">
                      <Progress value={65} className="w-full" />
                      <p className="text-sm text-muted-foreground mt-2">Scanning in progress...</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

// Findings Component  
const Findings = () => {
  const [findings, setFindings] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [showRemediationDialog, setShowRemediationDialog] = useState(false);
  const [remediation, setRemediation] = useState(null);
  const [filters, setFilters] = useState({
    severity: '',
    asset_id: ''
  });

  useEffect(() => {
    fetchFindings();
    fetchAssets();
  }, [filters]);

  const fetchFindings = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.severity) params.append('severity', filters.severity);
      if (filters.asset_id) params.append('asset_id', filters.asset_id);
      
      const response = await axios.get(`${API}/findings?${params}`);
      setFindings(response.data);
    } catch (error) {
      console.error('Failed to fetch findings:', error);
      toast.error('Failed to load findings');
    } finally {
      setLoading(false);
    }
  };

  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${API}/assets`);
      setAssets(response.data);
    } catch (error) {
      console.error('Failed to fetch assets:', error);
    }
  };

  const analyzeVulnerability = async (findingId) => {
    try {
      const response = await axios.post(`${API}/findings/${findingId}/analyze`);
      toast.success('AI analysis completed');
      return response.data;
    } catch (error) {
      console.error('Analysis failed:', error);
      toast.error('Failed to analyze vulnerability');
    }
  };

  const generateRemediation = async (findingId) => {
    try {
      const response = await axios.post(`${API}/findings/${findingId}/remediation`);
      setRemediation(response.data);
      setShowRemediationDialog(true);
      toast.success('Remediation playbook generated');
    } catch (error) {
      console.error('Remediation generation failed:', error);
      toast.error('Failed to generate remediation');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Security Findings</h1>
          <p className="text-muted-foreground">Vulnerability findings and remediation guidance</p>
        </div>
        <div className="flex gap-2">
          <Select value={filters.severity} onValueChange={(value) => setFilters({...filters, severity: value})}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by severity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All Severities</SelectItem>
              <SelectItem value="critical">Critical</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            More Filters
          </Button>
        </div>
      </div>

      <div className="space-y-4">
        {findings.map((finding) => {
          const asset = assets.find(a => a.id === finding.asset_id);
          return (
            <Card key={finding.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Badge variant={SEVERITY_BADGES[finding.severity]}>
                        {finding.severity.toUpperCase()}
                      </Badge>
                      <h3 className="text-lg font-semibold">{finding.title}</h3>
                    </div>
                    <p className="text-muted-foreground mb-3">{finding.description}</p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Asset:</span>
                        <p className="font-medium">{asset?.hostname || 'Unknown'}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">CVE IDs:</span>
                        <p className="font-medium">
                          {finding.cve_ids?.length > 0 ? finding.cve_ids.join(', ') : 'N/A'}
                        </p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Risk Score:</span>
                        <p className="font-medium">{finding.risk_score?.toFixed(1) || 'N/A'}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">First Seen:</span>
                        <p className="font-medium">{new Date(finding.first_seen).toLocaleDateString()}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex gap-2 ml-4">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => analyzeVulnerability(finding.id)}
                    >
                      <Zap className="h-4 w-4 mr-2" />
                      AI Analysis
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => generateRemediation(finding.id)}
                    >
                      <Settings className="h-4 w-4 mr-2" />
                      Remediate
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedFinding(finding)}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Remediation Dialog */}
      <Dialog open={showRemediationDialog} onOpenChange={setShowRemediationDialog}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>Remediation Playbook</DialogTitle>
            <DialogDescription>
              AI-generated remediation guidance and scripts
            </DialogDescription>
          </DialogHeader>
          {remediation && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Estimated Time:</span>
                  <p className="font-medium">{remediation.estimated_time} minutes</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Risk Level:</span>
                  <Badge variant={SEVERITY_BADGES[remediation.risk_level]}>
                    {remediation.risk_level.toUpperCase()}
                  </Badge>
                </div>
              </div>

              <Tabs defaultValue="manual" className="w-full">
                <TabsList>
                  <TabsTrigger value="manual">Manual Steps</TabsTrigger>
                  <TabsTrigger value="ansible">Ansible</TabsTrigger>
                  <TabsTrigger value="powershell">PowerShell</TabsTrigger>
                  <TabsTrigger value="bash">Bash Script</TabsTrigger>
                </TabsList>

                <TabsContent value="manual" className="space-y-4">
                  <div className="bg-slate-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-3">Step-by-Step Instructions</h4>
                    <ol className="space-y-2">
                      {remediation.manual_steps?.map((step, index) => (
                        <li key={index} className="flex gap-3">
                          <span className="bg-blue-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                            {index + 1}
                          </span>
                          <span>{step}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                </TabsContent>

                <TabsContent value="ansible">
                  <div className="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.ansible_playbook || 'No Ansible playbook available'}</pre>
                  </div>
                </TabsContent>

                <TabsContent value="powershell">
                  <div className="bg-blue-900 text-blue-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.powershell_script || 'No PowerShell script available'}</pre>
                  </div>
                </TabsContent>

                <TabsContent value="bash">
                  <div className="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.bash_script || 'No Bash script available'}</pre>
                  </div>
                </TabsContent>
              </Tabs>

              <div className="flex gap-2">
                <Button>
                  <Download className="h-4 w-4 mr-2" />
                  Download Playbook
                </Button>
                <Button variant="outline">
                  <Play className="h-4 w-4 mr-2" />
                  Execute
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

// Reports Component
const Reports = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Security Reports</h1>
        <p className="text-muted-foreground">Comprehensive security analytics and reporting</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Executive Summary</CardTitle>
            <CardDescription>High-level security posture overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <FileText className="h-8 w-8 text-blue-600" />
              <div>
                <p className="font-medium">Latest: Dec 2024</p>
                <p className="text-sm text-muted-foreground">12 pages • PDF</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Technical Report</CardTitle>
            <CardDescription>Detailed vulnerability analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <BarChart3 className="h-8 w-8 text-green-600" />
              <div>
                <p className="font-medium">Latest: Dec 2024</p>
                <p className="text-sm text-muted-foreground">45 pages • PDF</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Compliance Report</CardTitle>
            <CardDescription>Regulatory compliance status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <CheckCircle className="h-8 w-8 text-purple-600" />
              <div>
                <p className="font-medium">Latest: Dec 2024</p>
                <p className="text-sm text-muted-foreground">8 pages • PDF</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate Custom Report</CardTitle>
          <CardDescription>Create tailored security reports</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Report Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select report type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="executive">Executive Summary</SelectItem>
                  <SelectItem value="technical">Technical Analysis</SelectItem>
                  <SelectItem value="compliance">Compliance Report</SelectItem>
                  <SelectItem value="custom">Custom Report</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Time Period</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select time period" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                  <SelectItem value="custom">Custom Range</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button>
            <FileText className="h-4 w-4 mr-2" />
            Generate Report
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50">
        <Navigation />
        <main className="ml-64 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/findings" element={<Findings />} />
            <Route path="/scans" element={<Scans />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </Router>
  );
}

export default App;