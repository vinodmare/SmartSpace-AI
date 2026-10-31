import {
  Activity,
  BadgeCheck,
  BarChart3,
  Building2,
  CalendarDays,
  CircleDollarSign,
  Clock,
  CreditCard,
  Heart,
  Home,
  LayoutDashboard,
  LineChart,
  LockKeyhole,
  MessageSquareText,
  ShieldAlert,
  Sparkles,
  Star,
  Users,
  Warehouse,
} from "lucide-react";

export const publicNav = [
  { label: "About", href: "/about" },
  { label: "Pricing", href: "/pricing" },
  { label: "FAQ", href: "/faq" },
  { label: "Contact", href: "/contact" },
];

export const customerNav = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Search Spaces", href: "/search", icon: Building2 },
  { label: "AI Search", href: "/ai-search", icon: Sparkles },
  { label: "Booking", href: "/booking", icon: CreditCard },
  { label: "Booking History", href: "/booking-history", icon: Clock },
  { label: "Favorites", href: "/favorites", icon: Heart },
  { label: "Notifications", href: "/notifications", icon: MessageSquareText },
  { label: "Profile", href: "/profile", icon: Users },
  { label: "Settings", href: "/settings", icon: LockKeyhole },
];

export const ownerNav = [
  { label: "Owner Dashboard", href: "/owner", icon: LayoutDashboard },
  { label: "Add Space", href: "/owner/spaces/add", icon: Home },
  { label: "Edit Space", href: "/owner/spaces/edit", icon: Building2 },
  { label: "Bookings", href: "/owner/bookings", icon: CalendarDays },
  { label: "Revenue Analytics", href: "/owner/revenue", icon: LineChart },
  { label: "Calendar", href: "/owner/calendar", icon: CalendarDays },
  { label: "AI Price", href: "/owner/ai-price", icon: Sparkles },
  { label: "Reviews", href: "/owner/reviews", icon: Star },
];

export const adminNav = [
  { label: "Admin Dashboard", href: "/admin", icon: LayoutDashboard },
  { label: "Users", href: "/admin/users", icon: Users },
  { label: "Owner Verification", href: "/admin/owner-verification", icon: BadgeCheck },
  { label: "Space Approval", href: "/admin/space-approval", icon: Building2 },
  { label: "Bookings", href: "/admin/bookings", icon: CalendarDays },
  { label: "Reports", href: "/admin/reports", icon: BarChart3 },
  { label: "Fraud Monitoring", href: "/admin/fraud", icon: ShieldAlert },
  { label: "Analytics", href: "/admin/analytics", icon: Activity },
];

export const spaces = [
  {
    id: "luma-hall",
    name: "Luma Grand Hall",
    type: "Event Hall",
    city: "San Francisco",
    price: 26000,
    rating: 4.9,
    capacity: 280,
    image:
      "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=1200&q=80",
    tags: ["Weddings", "AV-ready", "Catering"],
    demand: 91,
  },
  {
    id: "northline-studio",
    name: "Northline Creator Studio",
    type: "Studio",
    city: "Austin",
    price: 7200,
    rating: 4.8,
    capacity: 24,
    image:
      "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1200&q=80",
    tags: ["Podcast", "Lighting", "Cyclorama"],
    demand: 84,
  },
  {
    id: "harbor-cowork",
    name: "Harbor Flex Cowork",
    type: "Coworking",
    city: "Seattle",
    price: 3500,
    rating: 4.7,
    capacity: 80,
    image:
      "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80",
    tags: ["Day pass", "Teams", "Coffee"],
    demand: 77,
  },
  {
    id: "atlas-warehouse",
    name: "Atlas Micro Warehouse",
    type: "Warehouse",
    city: "Chicago",
    price: 11500,
    rating: 4.6,
    capacity: 1200,
    image:
      "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80",
    tags: ["Loading dock", "Climate", "Secure"],
    demand: 69,
  },
];

export const stats = [
  { label: "AI matched bookings", value: "18,420", delta: "+24%", icon: Sparkles },
  { label: "Active spaces", value: "7,816", delta: "+13%", icon: Warehouse },
  { label: "Owner revenue", value: "₹10.6Cr", delta: "+19%", icon: CircleDollarSign },
  { label: "Fraud prevented", value: "₹6.9Cr", delta: "+31%", icon: ShieldAlert },
];

export const chartData = [42, 58, 44, 72, 66, 88, 79, 94, 83, 103, 118, 126];

export const bookings = [
  { guest: "Maya Patel", space: "Luma Grand Hall", date: "Jul 21", amount: "₹1,86,000", status: "Confirmed" },
  { guest: "Ethan Brooks", space: "Harbor Flex Cowork", date: "Jul 24", amount: "₹34,900", status: "Pending" },
  { guest: "Nora Kim", space: "Atlas Micro Warehouse", date: "Aug 02", amount: "₹1,63,000", status: "Review" },
  { guest: "Diego Ruiz", space: "Northline Creator Studio", date: "Aug 08", amount: "₹58,500", status: "Confirmed" },
];

export const faqs = [
  {
    q: "How does AI search work?",
    a: "SmartSpace AI converts natural language needs into space type, budget, capacity, location, amenities, and availability filters.",
  },
  {
    q: "Can owners set dynamic prices?",
    a: "Yes. The UI includes demand forecasting, competitor signals, and explainable price suggestions for every listed space.",
  },
  {
    q: "Is this backend-ready?",
    a: "The frontend is structured around mock data and reusable components so API, auth, and ML integrations can be connected later.",
  },
];
