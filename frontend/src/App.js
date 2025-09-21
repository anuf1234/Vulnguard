import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Enhanced state for comprehensive features
const useComplianceState = () => {
  const [complianceFrameworks, setComplianceFrameworks] = useState([]);
  const [complianceAssessments, setComplianceAssessments] = useState([]);
  const [gapAnalysis, setGapAnalysis] = useState(null);
  
  return {
    complianceFrameworks,
    setComplianceFrameworks,
    complianceAssessments,
    setComplianceAssessments,
    gapAnalysis,
    setGapAnalysis
  };
};

const useRiskState = () => {
  const [riskAssessments, setRiskAssessments] = useState([]);
  const [prioritizedFindings, setPrioritizedFindings] = useState([]);
  
  return {
    riskAssessments,
    setRiskAssessments,
    prioritizedFindings,
    setPrioritizedFindings
  };
};

const useRemediationState = () => {
  const [remediationTemplates, setRemediationTemplates] = useState([]);
  const [automatedRemediations, setAutomatedRemediations] = useState([]);
  
  return {
    remediationTemplates,
    setRemediationTemplates,
    automatedRemediations,
    setAutomatedRemediations
  };
};

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
  Filter,
  GitBranch,
  Ticket,
  History,
  Code,
  Terminal,
  PlayCircle,
  CheckSquare,
  AlertCircle,
  ShieldCheck,
  Network,
  Layers,
  GitPullRequest,
  UserCheck,
  Calendar,
  Globe,
  // New icons for enhanced features
  BookOpen,
  TrendingDown,
  Gauge,
  Cpu,
  Monitor,
  Building,
  UserPlus,
  Lock,
  Unlock,
  Key,
  FileCode,
  Workflow,
  Integration,
  Puzzle,
  Crown,
  Award,
  Briefcase,
  Radar,
  Flame,
  Crosshair,
  ShieldAlert,
  RefreshCw,
  FastForward,
  Layers3,
  CircuitBoard,
  CloudCog,
  HardDrive,
  Wifi,
  Smartphone,
  Laptop,
  TabletSmartphone
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
import { Switch } from './components/ui/switch';
import { Separator } from './components/ui/separator';

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

const FINDING_TYPE_COLORS = {
  vulnerability: '#dc2626',
  misconfiguration: '#ea580c',
  compliance: '#7c3aed',
  policy_violation: '#be185d'
};

// Navigation Component
const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/assets', icon: Server, label: 'Assets' },
    { path: '/findings', icon: AlertTriangle, label: 'Findings' },
    { path: '/scans', icon: Search, label: 'Scans' },
    { path: '/compliance', icon: Shield, label: 'Compliance', isNew: true },
    { path: '/risk-prioritization', icon: Flame, label: 'Risk Priority', isNew: true },
    { path: '/remediation', icon: Code, label: 'Remediation' },
    { path: '/change-management', icon: GitBranch, label: 'Change Mgmt' },
    { path: '/audit', icon: History, label: 'Audit Trail' },
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
            <p className="text-sm text-slate-400">Security Platform v2.0</p>
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
                className={`flex items-center justify-between px-4 py-3 rounded-lg transition-colors ${
                  isActive 
                    ? 'bg-red-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="h-5 w-5" />
                  {item.label}
                </div>
                {item.isNew && (
                  <Badge variant="secondary" className="bg-green-500 text-white text-xs px-2 py-0.5">
                    NEW
                  </Badge>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

// Enhanced Dashboard Component
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

  const findingTypeData = stats?.finding_types ? Object.entries(stats.finding_types).map(([key, value]) => ({
    name: key === 'policy_violation' ? 'Policy' : key.charAt(0).toUpperCase() + key.slice(1),
    value,
    color: FINDING_TYPE_COLORS[key]
  })) : [];

  const trendData = [
    { month: 'Jan', vulnerabilities: 45, misconfigurations: 23, resolved: 32 },
    { month: 'Feb', vulnerabilities: 52, misconfigurations: 31, resolved: 28 },
    { month: 'Mar', vulnerabilities: 61, misconfigurations: 28, resolved: 45 },
    { month: 'Apr', vulnerabilities: 38, misconfigurations: 19, resolved: 52 },
    { month: 'May', vulnerabilities: 73, misconfigurations: 35, resolved: 41 },
    { month: 'Jun', vulnerabilities: 42, misconfigurations: 22, resolved: 65 }
  ];

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-8 text-white overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Advanced Vulnerability Management Dashboard</h1>
              <p className="text-slate-300 text-lg">
                Comprehensive security posture with AI-powered analysis and automated remediation
              </p>
              <div className="flex items-center gap-4 mt-4">
                <Badge variant="secondary" className="bg-green-500/20 text-green-400">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Ansible Ready
                </Badge>
                <Badge variant="secondary" className="bg-blue-500/20 text-blue-400">
                  <ShieldCheck className="h-3 w-3 mr-1" />
                  AI Analysis
                </Badge>
                <Badge variant="secondary" className="bg-purple-500/20 text-purple-400">
                  <GitBranch className="h-3 w-3 mr-1" />
                  Change Mgmt
                </Badge>
              </div>
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

      {/* Enhanced Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-l-4 border-l-red-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.summary?.total_assets || 0}</div>
            <p className="text-xs text-muted-foreground">Infrastructure endpoints</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-orange-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Findings</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.summary?.total_findings || 0}</div>
            <p className="text-xs text-muted-foreground">
              {stats?.compliance_status?.misconfigurations || 0} misconfigurations
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cross-Host Vulns</CardTitle>
            <Network className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              {stats?.summary?.cross_host_vulnerabilities || 0}
            </div>
            <p className="text-xs text-muted-foreground">Multi-system impact</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-600">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Approvals</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {stats?.summary?.pending_approvals || 0}
            </div>
            <p className="text-xs text-muted-foreground">Change requests</p>
          </CardContent>
        </Card>
      </div>

      {/* Enhanced Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Security Trends</CardTitle>
            <CardDescription>Vulnerabilities, misconfigurations, and resolution rates</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="vulnerabilities" stackId="1" stroke="#dc2626" fill="#dc2626" fillOpacity={0.6} />
                <Area type="monotone" dataKey="misconfigurations" stackId="2" stroke="#ea580c" fill="#ea580c" fillOpacity={0.6} />
                <Area type="monotone" dataKey="resolved" stackId="3" stroke="#16a34a" fill="#16a34a" fillOpacity={0.6} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Finding Types Distribution</CardTitle>
            <CardDescription>Breakdown by vulnerability, misconfiguration, and compliance</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={findingTypeData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label
                >
                  {findingTypeData.map((entry, index) => (
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

      {/* Recent Activity and Change Management */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Activities</CardTitle>
            <CardDescription>Latest security operations and audit events</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {stats?.recent_activities?.slice(0, 5).map((activity) => (
                <div key={activity.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-full ${
                      activity.action === 'create' ? 'bg-green-100 text-green-600' :
                      activity.action === 'scan' ? 'bg-blue-100 text-blue-600' :
                      activity.action === 'approve' ? 'bg-purple-100 text-purple-600' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      {activity.action === 'create' ? <CheckCircle className="h-4 w-4" /> :
                       activity.action === 'scan' ? <Search className="h-4 w-4" /> :
                       activity.action === 'approve' ? <UserCheck className="h-4 w-4" /> :
                       <Activity className="h-4 w-4" />}
                    </div>
                    <div>
                      <p className="font-medium capitalize">{activity.action} {activity.resource_type}</p>
                      <p className="text-sm text-muted-foreground">
                        by {activity.user_id} • {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Ansible Remediation Stats</CardTitle>
            <CardDescription>Automated remediation capabilities and success rates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-green-100 text-green-600 p-2 rounded-full">
                    <Code className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="font-medium">Playbooks Generated</p>
                    <p className="text-sm text-muted-foreground">{stats?.summary?.total_remediations || 0} available</p>
                  </div>
                </div>
                <Badge variant="secondary" className="bg-green-100 text-green-700">
                  94% Success Rate
                </Badge>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-100 text-blue-600 p-2 rounded-full">
                    <Terminal className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="font-medium">Guided Execution</p>
                    <p className="text-sm text-muted-foreground">Step-by-step automation</p>
                  </div>
                </div>
                <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                  Available
                </Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-purple-100 text-purple-600 p-2 rounded-full">
                    <GitBranch className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="font-medium">Change Requests</p>
                    <p className="text-sm text-muted-foreground">{stats?.summary?.change_requests || 0} total</p>
                  </div>
                </div>
                <Badge variant="secondary" className="bg-purple-100 text-purple-700">
                  {stats?.summary?.pending_approvals || 0} Pending
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// Enhanced Assets Component with Inventory Management
const Assets = () => {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [filters, setFilters] = useState({
    environment: 'all',
    business_unit: 'all'
  });
  const [newAsset, setNewAsset] = useState({
    hostname: '',
    ip_address: '',
    asset_type: 'server',
    owner: '',
    environment: 'production',
    criticality: 3,
    operating_system: '',
    location: '',
    business_unit: '',
    compliance_requirements: []
  });

  useEffect(() => {
    fetchAssets();
  }, [filters]);

  const fetchAssets = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.environment && filters.environment !== 'all') params.append('environment', filters.environment);
      if (filters.business_unit && filters.business_unit !== 'all') params.append('business_unit', filters.business_unit);
      
      const response = await axios.get(`${API}/assets?${params}`);
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
        criticality: 3,
        operating_system: '',
        location: '',
        business_unit: '',
        compliance_requirements: []
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
          <h1 className="text-3xl font-bold">Asset Inventory Management</h1>
          <p className="text-muted-foreground">Manage infrastructure assets with compliance tracking</p>
        </div>
        <div className="flex gap-2">
          <Select value={filters.environment} onValueChange={(value) => setFilters({...filters, environment: value})}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by environment" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Environments</SelectItem>
              <SelectItem value="production">Production</SelectItem>
              <SelectItem value="staging">Staging</SelectItem>
              <SelectItem value="development">Development</SelectItem>
            </SelectContent>
          </Select>
          <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
            <DialogTrigger asChild>
              <Button>
                <Target className="h-4 w-4 mr-2" />
                Add Asset
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Add New Asset</DialogTitle>
                <DialogDescription>
                  Register a new asset with comprehensive inventory details
                </DialogDescription>
              </DialogHeader>
              <div className="grid grid-cols-2 gap-4">
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
                  <Label htmlFor="operating_system">Operating System</Label>
                  <Input
                    id="operating_system"
                    value={newAsset.operating_system}
                    onChange={(e) => setNewAsset({...newAsset, operating_system: e.target.value})}
                    placeholder="Ubuntu 20.04 LTS"
                  />
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
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={newAsset.location}
                    onChange={(e) => setNewAsset({...newAsset, location: e.target.value})}
                    placeholder="Data Center A"
                  />
                </div>
                <div>
                  <Label htmlFor="business_unit">Business Unit</Label>
                  <Input
                    id="business_unit"
                    value={newAsset.business_unit}
                    onChange={(e) => setNewAsset({...newAsset, business_unit: e.target.value})}
                    placeholder="Finance"
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
                <div className="col-span-2">
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
              </div>
              <Button onClick={handleAddAsset} className="w-full mt-4">
                Add Asset
              </Button>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {assets.map((asset) => (
          <Card key={asset.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{asset.hostname}</CardTitle>
                <div className="flex gap-2">
                  <Badge variant={asset.environment === 'production' ? 'destructive' : 'secondary'}>
                    {asset.environment}
                  </Badge>
                  {asset.compliance_requirements?.length > 0 && (
                    <Badge variant="outline">
                      <ShieldCheck className="h-3 w-3 mr-1" />
                      Compliance
                    </Badge>
                  )}
                </div>
              </div>
              <CardDescription>
                {asset.ip_address} • {asset.operating_system || 'OS not specified'}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Type:</span>
                  <p className="font-medium capitalize">{asset.asset_type.replace('_', ' ')}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Owner:</span>
                  <p className="font-medium">{asset.owner || 'Unassigned'}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Business Unit:</span>
                  <p className="font-medium">{asset.business_unit || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-muted-foreground">Location:</span>
                  <p className="font-medium">{asset.location || 'N/A'}</p>
                </div>
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
                  View Details
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

// Enhanced Scans Component with Misconfiguration Detection
const Scans = () => {
  const [scans, setScans] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewScan, setShowNewScan] = useState(false);
  const [showConfigScan, setShowConfigScan] = useState(false);
  const [newScan, setNewScan] = useState({
    name: '',
    targets: '',
    scan_type: 'network',
    include_misconfigs: true
  });

  useEffect(() => {
    fetchScans();
    fetchAssets();
  }, []);

  const fetchScans = async () => {
    try {
      setScans([
        {
          id: '1',
          name: 'Production Network Scan',
          scan_type: 'network',
          status: 'completed',
          findings_count: 23,
          misconfigs_count: 12,
          started_at: new Date().toISOString(),
          completed_at: new Date().toISOString()
        },
        {
          id: '2',
          name: 'Compliance Audit - CIS',
          scan_type: 'compliance',
          status: 'running',
          findings_count: 0,
          misconfigs_count: 0,
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

  const handleNetworkScan = async () => {
    try {
      const targets = newScan.targets.split(',').map(t => t.trim());
      const response = await axios.post(`${API}/scan/network`, {
        targets,
        scan_name: newScan.name,
        include_misconfigs: newScan.include_misconfigs
      });
      
      toast.success(`Network scan completed: ${response.data.findings_count} findings, ${response.data.misconfigurations || 0} misconfigurations`);
      setShowNewScan(false);
      setNewScan({
        name: '',
        targets: '',
        scan_type: 'network',
        include_misconfigs: true
      });
      fetchScans();
    } catch (error) {
      console.error('Network scan failed:', error);
      toast.error('Failed to start network scan');
    }
  };

  const handleComplianceScan = async () => {
    try {
      const assetIds = assets.slice(0, 3).map(a => a.id); // Select first 3 assets for demo
      const response = await axios.post(`${API}/scan/compliance`, {
        asset_ids: assetIds,
        framework: 'CIS'
      });
      
      toast.success(`Compliance scan completed: ${response.data.violations_found} violations found`);
      fetchScans();
    } catch (error) {
      console.error('Compliance scan failed:', error);
      toast.error('Failed to start compliance scan');
    }
  };

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
            Upload vulnerability scan files with misconfiguration detection
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

  const handleFileUpload = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('scan_name', `File Upload - ${file.name}`);
    formData.append('asset_id', assets[0]?.id || 'demo-asset');

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
          <h1 className="text-3xl font-bold">Advanced Security Scanning</h1>
          <p className="text-muted-foreground">Vulnerability and misconfiguration detection with compliance scanning</p>
        </div>
        <div className="flex gap-2">
          <Dialog open={showNewScan} onOpenChange={setShowNewScan}>
            <DialogTrigger asChild>
              <Button>
                <Play className="h-4 w-4 mr-2" />
                Network Scan
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Start Network Scan</DialogTitle>
                <DialogDescription>
                  Configure comprehensive network vulnerability and misconfiguration scan
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="scan_name">Scan Name</Label>
                  <Input
                    id="scan_name"
                    value={newScan.name}
                    onChange={(e) => setNewScan({...newScan, name: e.target.value})}
                    placeholder="Production Network Security Scan"
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
                <div className="flex items-center space-x-2">
                  <Switch
                    id="include_misconfigs"
                    checked={newScan.include_misconfigs}
                    onCheckedChange={(checked) => setNewScan({...newScan, include_misconfigs: checked})}
                  />
                  <Label htmlFor="include_misconfigs">Include misconfiguration detection</Label>
                </div>
                <Button onClick={handleNetworkScan} className="w-full">
                  Start Network Scan
                </Button>
              </div>
            </DialogContent>
          </Dialog>
          
          <Button variant="outline" onClick={handleComplianceScan}>
            <ShieldCheck className="h-4 w-4 mr-2" />
            Compliance Scan
          </Button>
        </div>
      </div>

      <Tabs defaultValue="upload" className="space-y-6">
        <TabsList>
          <TabsTrigger value="upload">File Upload</TabsTrigger>
          <TabsTrigger value="history">Scan History</TabsTrigger>
          <TabsTrigger value="compliance">Compliance</TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <FileUploadCard onFileUpload={handleFileUpload} />
            
            <Card>
              <CardHeader>
                <CardTitle>Enhanced Scan Capabilities</CardTitle>
                <CardDescription>Advanced detection and analysis features</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                  <div>
                    <p className="font-medium">Vulnerability Detection</p>
                    <p className="text-sm text-muted-foreground">CVE-based vulnerability identification</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-lg">
                  <Settings className="h-5 w-5 text-orange-600" />
                  <div>
                    <p className="font-medium">Misconfiguration Detection</p>
                    <p className="text-sm text-muted-foreground">AI-powered configuration analysis</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                  <ShieldCheck className="h-5 w-5 text-purple-600" />
                  <div>
                    <p className="font-medium">Compliance Scanning</p>
                    <p className="text-sm text-muted-foreground">CIS, NIST, PCI-DSS benchmarks</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <Code className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="font-medium">Ansible Remediation</p>
                    <p className="text-sm text-muted-foreground">Automated playbook generation</p>
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
                        <div className="flex items-center gap-4 text-muted-foreground">
                          <span>{scan.scan_type} scan</span>
                          <span>•</span>
                          <span>{scan.findings_count} vulnerabilities</span>
                          {scan.misconfigs_count > 0 && (
                            <>
                              <span>•</span>
                              <span>{scan.misconfigs_count} misconfigurations</span>
                            </>
                          )}
                        </div>
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

        <TabsContent value="compliance" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ShieldCheck className="h-5 w-5 text-blue-600" />
                  CIS Benchmarks
                </CardTitle>
                <CardDescription>Center for Internet Security guidelines</CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={handleComplianceScan} className="w-full" variant="outline">
                  Run CIS Scan
                </Button>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-purple-600" />
                  NIST Framework
                </CardTitle>
                <CardDescription>NIST Cybersecurity Framework</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Run NIST Scan
                </Button>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5 text-green-600" />
                  PCI-DSS
                </CardTitle>
                <CardDescription>Payment Card Industry standards</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Run PCI Scan
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

// Enhanced Findings Component with Cross-Host Tracking
const Findings = () => {
  const [findings, setFindings] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [showRemediationDialog, setShowRemediationDialog] = useState(false);
  const [remediation, setRemediation] = useState(null);
  const [filters, setFilters] = useState({
    severity: 'all',
    finding_type: 'all',
    cross_host: false
  });

  useEffect(() => {
    fetchFindings();
    fetchAssets();
  }, [filters]);

  const fetchFindings = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.severity && filters.severity !== 'all') params.append('severity', filters.severity);
      if (filters.finding_type && filters.finding_type !== 'all') params.append('finding_type', filters.finding_type);
      if (filters.cross_host) params.append('cross_host', 'true');
      
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

  const generateAnsibleRemediation = async (findingId, guided = false) => {
    try {
      const response = await axios.post(`${API}/findings/${findingId}/remediation/ansible?guided=${guided}`);
      setRemediation(response.data);
      setShowRemediationDialog(true);
      toast.success('Ansible remediation playbook generated');
    } catch (error) {
      console.error('Ansible remediation generation failed:', error);
      toast.error('Failed to generate Ansible remediation');
    }
  };

  const createChangeRequest = async (remediationId) => {
    try {
      const response = await axios.post(`${API}/change-requests`, {
        title: `Security Remediation: ${selectedFinding?.title}`,
        description: `Automated remediation for security finding: ${selectedFinding?.description}`,
        remediation_id: remediationId,
        requestor: 'security-team',
        priority: selectedFinding?.severity || 'medium'
      });
      toast.success('Change request created successfully');
      return response.data;
    } catch (error) {
      console.error('Change request creation failed:', error);
      toast.error('Failed to create change request');
    }
  };

  const createTicket = async (findingId, remediationId) => {
    try {
      const response = await axios.post(`${API}/tickets`, {
        title: `Security Finding: ${selectedFinding?.title}`,
        description: `${selectedFinding?.description}\n\nRemediation playbook available.`,
        finding_id: findingId,
        remediation_id: remediationId,
        priority: selectedFinding?.severity || 'medium',
        external_system: 'jira'
      });
      toast.success('Ticket created successfully');
      return response.data;
    } catch (error) {
      console.error('Ticket creation failed:', error);
      toast.error('Failed to create ticket');
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
          <h1 className="text-3xl font-bold">Security Findings & Cross-Host Analysis</h1>
          <p className="text-muted-foreground">AI-powered vulnerability analysis with automated Ansible remediation</p>
        </div>
        <div className="flex gap-2">
          <Select value={filters.severity} onValueChange={(value) => setFilters({...filters, severity: value})}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by severity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Severities</SelectItem>
              <SelectItem value="critical">Critical</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
            </SelectContent>
          </Select>
          <Select value={filters.finding_type} onValueChange={(value) => setFilters({...filters, finding_type: value})}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="vulnerability">Vulnerabilities</SelectItem>
              <SelectItem value="misconfiguration">Misconfigurations</SelectItem>
              <SelectItem value="compliance">Compliance</SelectItem>
            </SelectContent>
          </Select>
          <Button
            variant={filters.cross_host ? "default" : "outline"}
            onClick={() => setFilters({...filters, cross_host: !filters.cross_host})}
          >
            <Network className="h-4 w-4 mr-2" />
            Cross-Host Only
          </Button>
        </div>
      </div>

      <div className="space-y-4">
        {findings.map((finding) => {
          const asset = assets.find(a => a.id === finding.asset_id);
          const isMultiHost = finding.affected_hosts?.length > 1;
          
          return (
            <Card key={finding.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Badge variant={SEVERITY_BADGES[finding.severity]}>
                        {finding.severity.toUpperCase()}
                      </Badge>
                      <Badge 
                        variant="outline" 
                        style={{ borderColor: FINDING_TYPE_COLORS[finding.finding_type] }}
                      >
                        {finding.finding_type.toUpperCase()}
                      </Badge>
                      {isMultiHost && (
                        <Badge variant="secondary" className="bg-purple-100 text-purple-700">
                          <Network className="h-3 w-3 mr-1" />
                          Multi-Host
                        </Badge>
                      )}
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
                        <span className="text-muted-foreground">Affected Hosts:</span>
                        <p className="font-medium">{finding.affected_hosts?.length || 1}</p>
                      </div>
                    </div>

                    {finding.compliance_frameworks?.length > 0 && (
                      <div className="mt-3">
                        <span className="text-muted-foreground text-sm">Compliance: </span>
                        {finding.compliance_frameworks.map(framework => (
                          <Badge key={framework} variant="outline" className="ml-1">
                            {framework}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col gap-2 ml-4">
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
                      onClick={() => {
                        setSelectedFinding(finding);
                        generateAnsibleRemediation(finding.id, false);
                      }}
                    >
                      <Code className="h-4 w-4 mr-2" />
                      Ansible
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setSelectedFinding(finding);
                        generateAnsibleRemediation(finding.id, true);
                      }}
                    >
                      <PlayCircle className="h-4 w-4 mr-2" />
                      Guided
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

      {/* Enhanced Remediation Dialog */}
      <Dialog open={showRemediationDialog} onOpenChange={setShowRemediationDialog}>
        <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Ansible Remediation Playbook</DialogTitle>
            <DialogDescription>
              AI-generated Ansible automation with guided execution and change management
            </DialogDescription>
          </DialogHeader>
          {remediation && (
            <div className="space-y-6">
              <div className="grid grid-cols-3 gap-4 text-sm">
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
                <div>
                  <span className="text-muted-foreground">Affected Systems:</span>
                  <p className="font-medium">{remediation.affected_systems?.length || 1}</p>
                </div>
              </div>

              <Tabs defaultValue="playbook" className="w-full">
                <TabsList className="grid w-full grid-cols-5">
                  <TabsTrigger value="playbook">Playbook</TabsTrigger>
                  <TabsTrigger value="inventory">Inventory</TabsTrigger>
                  <TabsTrigger value="guided">Guided Steps</TabsTrigger>
                  <TabsTrigger value="validation">Validation</TabsTrigger>
                  <TabsTrigger value="rollback">Rollback</TabsTrigger>
                </TabsList>

                <TabsContent value="playbook" className="space-y-4">
                  <div className="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.ansible_playbook || 'No Ansible playbook available'}</pre>
                  </div>
                </TabsContent>

                <TabsContent value="inventory" className="space-y-4">
                  <div className="bg-slate-900 text-blue-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.ansible_inventory || 'No inventory file available'}</pre>
                  </div>
                </TabsContent>

                <TabsContent value="guided" className="space-y-4">
                  <div className="bg-slate-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-3">Guided Execution Steps</h4>
                    <div className="space-y-3">
                      {remediation.guided_steps?.map((step, index) => (
                        <div key={index} className="flex gap-3 p-3 bg-white rounded border">
                          <span className="bg-blue-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                            {index + 1}
                          </span>
                          <div className="flex-1">
                            <p className="font-medium">{step.title || `Step ${index + 1}`}</p>
                            <p className="text-sm text-muted-foreground">{step.description || step}</p>
                            {step.command && (
                              <code className="block mt-2 p-2 bg-gray-100 rounded text-sm">
                                {step.command}
                              </code>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="validation" className="space-y-4">
                  <div className="space-y-3">
                    <h4 className="font-medium">Pre-execution Validation Checks</h4>
                    {remediation.validation_checks?.map((check, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                        <span>{check}</span>
                      </div>
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="rollback" className="space-y-4">
                  <div className="bg-red-900 text-red-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                    <pre>{remediation.rollback_plan || 'No rollback plan available'}</pre>
                  </div>
                </TabsContent>
              </Tabs>

              <Separator />

              <div className="flex flex-wrap gap-2">
                <Button>
                  <Download className="h-4 w-4 mr-2" />
                  Download Playbook
                </Button>
                <Button variant="outline">
                  <Terminal className="h-4 w-4 mr-2" />
                  Execute Locally
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => createChangeRequest(remediation.id)}
                >
                  <GitBranch className="h-4 w-4 mr-2" />
                  Create Change Request
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => createTicket(selectedFinding?.id, remediation.id)}
                >
                  <Ticket className="h-4 w-4 mr-2" />
                  Create Ticket
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

// New Change Management Component
const ChangeManagement = () => {
  const [changeRequests, setChangeRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChangeRequests();
  }, []);

  const fetchChangeRequests = async () => {
    try {
      const response = await axios.get(`${API}/change-requests`);
      setChangeRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch change requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const approveChangeRequest = async (requestId) => {
    try {
      await axios.post(`${API}/change-requests/${requestId}/approve`, {
        approver: 'security-manager',
        approval_notes: 'Approved for execution during maintenance window'
      });
      toast.success('Change request approved');
      fetchChangeRequests();
    } catch (error) {
      console.error('Failed to approve change request:', error);
      toast.error('Failed to approve change request');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Change Management</h1>
          <p className="text-muted-foreground">Approval workflows for security remediation</p>
        </div>
      </div>

      <div className="space-y-4">
        {changeRequests.map((request) => (
          <Card key={request.id}>
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Badge variant={request.status === 'approved' ? 'default' : 'secondary'}>
                      {request.status.toUpperCase()}
                    </Badge>
                    <Badge variant={SEVERITY_BADGES[request.priority]}>
                      {request.priority.toUpperCase()}
                    </Badge>
                    <h3 className="text-lg font-semibold">{request.title}</h3>
                  </div>
                  <p className="text-muted-foreground mb-3">{request.description}</p>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Requestor:</span>
                      <p className="font-medium">{request.requestor}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Affected Systems:</span>
                      <p className="font-medium">{request.affected_systems?.length || 0}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Created:</span>
                      <p className="font-medium">{new Date(request.created_at).toLocaleDateString()}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Scheduled:</span>
                      <p className="font-medium">
                        {request.scheduled_time ? new Date(request.scheduled_time).toLocaleDateString() : 'Not scheduled'}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2 ml-4">
                  {request.status === 'pending' && (
                    <Button
                      size="sm"
                      onClick={() => approveChangeRequest(request.id)}
                    >
                      <UserCheck className="h-4 w-4 mr-2" />
                      Approve
                    </Button>
                  )}
                  <Button variant="outline" size="sm">
                    <Eye className="h-4 w-4 mr-2" />
                    View Details
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

// New Audit Trail Component
const AuditTrail = () => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    action: 'all',
    resource_type: 'all'
  });

  useEffect(() => {
    fetchAuditLogs();
  }, [filters]);

  const fetchAuditLogs = async () => {  
    try {
      const params = new URLSearchParams();
      if (filters.action && filters.action !== 'all') params.append('action', filters.action);
      if (filters.resource_type && filters.resource_type !== 'all') params.append('resource_type', filters.resource_type);
      
      const response = await axios.get(`${API}/audit-logs?${params}`);
      setAuditLogs(response.data);
    } catch (error) {
      console.error('Failed to fetch audit logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'create': return <CheckCircle className="h-4 w-4" />;
      case 'scan': return <Search className="h-4 w-4" />;
      case 'approve': return <UserCheck className="h-4 w-4" />;
      case 'remediate': return <Code className="h-4 w-4" />;
      default: return <Activity className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Audit Trail</h1>
          <p className="text-muted-foreground">Complete security operations audit log</p>
        </div>
        <div className="flex gap-2">
          <Select value={filters.action} onValueChange={(value) => setFilters({...filters, action: value})}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by action" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Actions</SelectItem>
              <SelectItem value="create">Create</SelectItem>
              <SelectItem value="scan">Scan</SelectItem>
              <SelectItem value="approve">Approve</SelectItem>
              <SelectItem value="remediate">Remediate</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-2">
        {auditLogs.map((log, index) => (
          <Card key={log.id} className="p-4">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="bg-slate-100 p-2 rounded-full">
                  {getActionIcon(log.action)}
                </div>
                <div>
                  <p className="font-medium capitalize">
                    {log.action} {log.resource_type}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    by {log.user_id} • {new Date(log.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
              <div className="ml-auto">
                <Badge variant="outline">
                  {log.resource_type}
                </Badge>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

// Enhanced Reports Component
const Reports = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Security Reports & Analytics</h1>
        <p className="text-muted-foreground">Comprehensive security reporting with compliance mapping</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Executive Dashboard</CardTitle>
            <CardDescription>High-level security posture and risk metrics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <BarChart3 className="h-8 w-8 text-blue-600" />
              <div>
                <p className="font-medium">Latest: Current</p>
                <p className="text-sm text-muted-foreground">Real-time data • Interactive</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Ansible Remediation Report</CardTitle>
            <CardDescription>Automation success rates and playbook effectiveness</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <Code className="h-8 w-8 text-green-600" />
              <div>
                <p className="font-medium">Success Rate: 94%</p>
                <p className="text-sm text-muted-foreground">45 playbooks executed</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Compliance Status</CardTitle>
            <CardDescription>CIS, NIST, PCI-DSS compliance overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <ShieldCheck className="h-8 w-8 text-purple-600" />
              <div>
                <p className="font-medium">87% Compliant</p>
                <p className="text-sm text-muted-foreground">Multi-framework assessment</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Cross-Host Analysis</CardTitle>
            <CardDescription>Multi-system vulnerability impact analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <Network className="h-8 w-8 text-orange-600" />
              <div>
                <p className="font-medium">12 Cross-Host Vulns</p>
                <p className="text-sm text-muted-foreground">Widespread impact assessment</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Change Management Report</CardTitle>
            <CardDescription>Approval workflows and remediation tracking</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <GitBranch className="h-8 w-8 text-indigo-600" />
              <div>
                <p className="font-medium">23 Changes This Month</p>
                <p className="text-sm text-muted-foreground">95% approval rate</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Audit Trail Summary</CardTitle>
            <CardDescription>Security operations audit and compliance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <History className="h-8 w-8 text-slate-600" />
              <div>
                <p className="font-medium">1,247 Events Logged</p>
                <p className="text-sm text-muted-foreground">Complete audit trail</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate Custom Report</CardTitle>
          <CardDescription>Create tailored security and compliance reports</CardDescription>
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
                  <SelectItem value="ansible">Ansible Automation Report</SelectItem>
                  <SelectItem value="cross-host">Cross-Host Analysis</SelectItem>
                  <SelectItem value="audit">Audit Trail Report</SelectItem>
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

// === COMPLIANCE MANAGEMENT COMPONENT ===
const ComplianceManagement = () => {
  const [frameworks, setFrameworks] = useState([]);
  const [selectedFramework, setSelectedFramework] = useState('');
  const [controls, setControls] = useState([]);
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('frameworks');

  useEffect(() => {
    fetchFrameworks();
    fetchAssessments();
  }, []);

  const fetchFrameworks = async () => {
    try {
      const response = await axios.get(`${API}/compliance/frameworks`);
      setFrameworks(response.data.frameworks);
    } catch (error) {
      console.error('Failed to fetch frameworks:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFrameworkControls = async (frameworkId) => {
    try {
      const response = await axios.get(`${API}/compliance/frameworks/${frameworkId}/controls`);
      setControls(response.data.controls);
    } catch (error) {
      console.error('Failed to fetch controls:', error);
    }
  };

  const performGapAnalysis = async (framework) => {
    try {
      const response = await axios.get(`${API}/compliance/gap-analysis/${framework}`);
      setGapAnalysis(response.data);
    } catch (error) {
      console.error('Failed to perform gap analysis:', error);
    }
  };

  const fetchAssessments = async () => {
    try {
      const response = await axios.get(`${API}/compliance/assessments`);
      setAssessments(response.data);
    } catch (error) {
      console.error('Failed to fetch assessments:', error);
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
          <h1 className="text-3xl font-bold">Compliance Management</h1>
          <p className="text-muted-foreground">Automated compliance mapping and gap analysis</p>
        </div>
        <Button>
          <Award className="h-4 w-4 mr-2" />
          New Assessment
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'frameworks', name: 'Frameworks', icon: BookOpen },
            { id: 'gap-analysis', name: 'Gap Analysis', icon: Radar },
            { id: 'assessments', name: 'Assessments', icon: CheckSquare }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-red-500 text-red-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Frameworks Tab */}
      {activeTab === 'frameworks' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {frameworks.map((framework) => (
              <Card key={framework.id} className="cursor-pointer hover:shadow-md transition-shadow"
                    onClick={() => {
                      setSelectedFramework(framework.id);
                      fetchFrameworkControls(framework.id);
                    }}>
                <CardHeader className="pb-3">
                  <div className="flex items-center gap-3">
                    <div className="bg-blue-100 text-blue-600 p-2 rounded-lg">
                      <Shield className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{framework.name}</CardTitle>
                      <CardDescription className="text-sm">{framework.controls_count} controls</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{framework.description}</p>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="mt-3"
                    onClick={(e) => {
                      e.stopPropagation();
                      performGapAnalysis(framework.id);
                      setActiveTab('gap-analysis');
                    }}
                  >
                    <Radar className="h-4 w-4 mr-2" />
                    Analyze Gaps
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Framework Controls */}
          {selectedFramework && controls.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Framework Controls - {frameworks.find(f => f.id === selectedFramework)?.name}</CardTitle>
                <CardDescription>Detailed control requirements and implementation guidance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {controls.map((control) => (
                    <div key={control.control_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Badge variant={control.priority === 'critical' ? 'destructive' : 
                                        control.priority === 'high' ? 'secondary' : 'outline'}>
                            {control.priority}
                          </Badge>
                          <h4 className="font-medium">{control.control_id}: {control.title}</h4>
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="h-4 w-4 mr-2" />
                          View Details
                        </Button>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2 mb-3">{control.family}</p>
                      <p className="text-sm">{control.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Gap Analysis Tab */}
      {activeTab === 'gap-analysis' && gapAnalysis && (
        <div className="space-y-6">
          {/* Compliance Score Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Gauge className="h-5 w-5" />
                Compliance Score - {gapAnalysis.framework.replace('_', ' ').toUpperCase()}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600">{gapAnalysis.compliance_score}%</div>
                  <p className="text-sm text-muted-foreground">Overall Compliance</p>
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-green-600">Compliant: {gapAnalysis.compliant_controls}</span>
                    <span className="text-yellow-600">Partial: {gapAnalysis.partial_compliance}</span>
                    <span className="text-red-600">Non-compliant: {gapAnalysis.non_compliant_controls}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 h-3 rounded-full"
                      style={{width: `${gapAnalysis.compliance_score}%`}}
                    ></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Control Status Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(gapAnalysis.control_details).slice(0, 9).map(([controlId, details]) => (
              <Card key={controlId} className={`border-l-4 ${
                details.status === 'compliant' ? 'border-l-green-500' :
                details.status === 'partial' ? 'border-l-yellow-500' : 'border-l-red-500'
              }`}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-medium">{controlId}</CardTitle>
                    <Badge variant={details.status === 'compliant' ? 'default' : 
                                  details.status === 'partial' ? 'secondary' : 'destructive'}>
                      {details.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">{details.control_title}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>Findings: {details.findings_count}</span>
                      <span className="text-red-600">Critical: {details.critical_findings}</span>
                    </div>
                    <p className="text-xs text-muted-foreground">{details.control_family}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Crosshair className="h-5 w-5" />
                Remediation Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {gapAnalysis.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">{rec}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Assessments Tab */}
      {activeTab === 'assessments' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Compliance Assessments</CardTitle>
              <CardDescription>Track formal compliance assessments and audits</CardDescription>
            </CardHeader>
            <CardContent>
              {assessments.length === 0 ? (
                <div className="text-center py-8">
                  <CheckSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-muted-foreground">No assessments created yet</p>
                  <Button className="mt-4">
                    <Award className="h-4 w-4 mr-2" />
                    Create First Assessment
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {assessments.map((assessment) => (
                    <div key={assessment.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium">{assessment.assessment_name}</h4>
                          <p className="text-sm text-muted-foreground">{assessment.framework} • {assessment.scope_description}</p>
                        </div>
                        <Badge variant={assessment.status === 'completed' ? 'default' : 'secondary'}>
                          {assessment.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

// === RISK PRIORITIZATION COMPONENT ===
const RiskPrioritization = () => {
  const [prioritizedFindings, setPrioritizedFindings] = useState([]);
  const [riskMetrics, setRiskMetrics] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [showRiskDialog, setShowRiskDialog] = useState(false);

  useEffect(() => {
    fetchPrioritizedFindings();
  }, []);

  const fetchPrioritizedFindings = async () => {
    try {
      const response = await axios.get(`${API}/risk/prioritized-findings`);
      setPrioritizedFindings(response.data.prioritized_findings);
      setRiskMetrics(response.data);
    } catch (error) {
      console.error('Failed to fetch prioritized findings:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateRisk = async (findingId) => {
    try {
      const response = await axios.post(`${API}/risk/calculate`, {
        finding_id: findingId,
        cvss_score: 7.5,
        epss_score: 0.3,
        kev_listed: false,
        asset_criticality: 'high',
        business_impact: 'high'
      });
      
      // Refresh findings after risk calculation
      fetchPrioritizedFindings();
      
      return response.data;
    } catch (error) {
      console.error('Failed to calculate risk:', error);
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
          <h1 className="text-3xl font-bold">Risk-Based Prioritization</h1>
          <p className="text-muted-foreground">AI-powered vulnerability risk assessment and prioritization</p>
        </div>
        <Button onClick={() => fetchPrioritizedFindings()}>
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh Analysis
        </Button>
      </div>

      {/* Risk Metrics Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Total Findings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Flame className="h-8 w-8 text-red-500" />
              <div>
                <div className="text-2xl font-bold">{riskMetrics.total_findings || 0}</div>
                <p className="text-sm text-muted-foreground">Risk assessed</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Critical Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <ShieldAlert className="h-8 w-8 text-purple-500" />
              <div>
                <div className="text-2xl font-bold text-purple-600">
                  {prioritizedFindings.filter(f => f.risk_score >= 0.8).length}
                </div>
                <p className="text-sm text-muted-foreground">Immediate action</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">High Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-8 w-8 text-orange-500" />
              <div>
                <div className="text-2xl font-bold text-orange-600">
                  {prioritizedFindings.filter(f => f.risk_score >= 0.6 && f.risk_score < 0.8).length}
                </div>
                <p className="text-sm text-muted-foreground">7-day SLA</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Avg Risk Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <Gauge className="h-8 w-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold text-blue-600">
                  {prioritizedFindings.length > 0 
                    ? (prioritizedFindings.reduce((sum, f) => sum + f.risk_score, 0) / prioritizedFindings.length * 100).toFixed(0)
                    : 0}%
                </div>
                <p className="text-sm text-muted-foreground">Risk level</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Prioritized Findings Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingDown className="h-5 w-5" />
            Risk-Prioritized Findings
          </CardTitle>
          <CardDescription>Findings ranked by comprehensive risk assessment</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {prioritizedFindings.map((finding, index) => (
              <div key={finding.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="text-center">
                      <div className="text-lg font-bold text-gray-600">#{finding.priority_rank}</div>
                      <div className="text-xs text-muted-foreground">Rank</div>
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium">{finding.title}</h4>
                        <Badge variant={finding.severity === 'critical' ? 'destructive' : 
                                      finding.severity === 'high' ? 'secondary' : 'outline'}>
                          {finding.severity}
                        </Badge>
                        {finding.cve_ids.length > 0 && (
                          <Badge variant="outline">
                            {finding.cve_ids.length} CVE{finding.cve_ids.length > 1 ? 's' : ''}
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">Asset ID: {finding.asset_id}</p>
                    </div>
                    
                    <div className="text-center">
                      <div className="flex items-center gap-2">
                        <div className={`text-lg font-bold ${
                          finding.risk_score >= 0.8 ? 'text-purple-600' :
                          finding.risk_score >= 0.6 ? 'text-red-600' :
                          finding.risk_score >= 0.4 ? 'text-orange-600' : 'text-yellow-600'
                        }`}>
                          {Math.round(finding.risk_score * 100)}%
                        </div>
                        <div className={`w-3 h-3 rounded-full ${
                          finding.risk_score >= 0.8 ? 'bg-purple-500' :
                          finding.risk_score >= 0.6 ? 'bg-red-500' :
                          finding.risk_score >= 0.4 ? 'bg-orange-500' : 'bg-yellow-500'
                        }`}></div>
                      </div>
                      <div className="text-xs text-muted-foreground">Risk Score</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm"
                            onClick={() => calculateRisk(finding.id)}>
                      <Crosshair className="h-4 w-4 mr-2" />
                      Recalculate
                    </Button>
                    <Button variant="outline" size="sm"
                            onClick={() => {
                              setSelectedFinding(finding);
                              setShowRiskDialog(true);
                            }}>
                      <Eye className="h-4 w-4 mr-2" />
                      Details
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Risk Factors Legend */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            Risk Assessment Methodology
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium mb-3">Risk Factors</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span>CVSS Base Score</span>
                  <span className="text-muted-foreground">25% weight</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>EPSS Exploit Likelihood</span>
                  <span className="text-muted-foreground">20% weight</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Asset Business Criticality</span>
                  <span className="text-muted-foreground">20% weight</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>CISA KEV Catalog</span>
                  <span className="text-muted-foreground">15% weight</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Business Impact</span>
                  <span className="text-muted-foreground">10% weight</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Compensating Controls</span>
                  <span className="text-muted-foreground">-10% weight</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium mb-3">Priority Categories</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                  <span>Critical (80-100%): Immediate action required</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <span>High (60-79%): 7-day remediation SLA</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                  <span>Medium (40-59%): 30-day remediation SLA</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <span>Low (0-39%): 90-day remediation SLA</span>
                </div>
              </div>
            </div>
          </div>
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
            <Route path="/change-management" element={<ChangeManagement />} />
            <Route path="/audit" element={<AuditTrail />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/compliance" element={<ComplianceManagement />} />
            <Route path="/risk-prioritization" element={<RiskPrioritization />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </Router>
  );
}

export default App;