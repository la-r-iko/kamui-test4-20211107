'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useMediaQuery,
  useTheme,
  Box,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  School as SchoolIcon,
  Book as BookIcon,
  AccountCircle as AccountIcon,
  AdminPanelSettings as AdminIcon,
} from '@mui/icons-material';

// ナビゲーション項目の型定義
interface NavItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  roles?: string[];
}

// ナビゲーション項目の定義
const navItems: NavItem[] = [
  { label: 'Home', path: '/', icon: <HomeIcon /> },
  { label: 'Lessons', path: '/lessons', icon: <SchoolIcon /> },
  { label: 'Materials', path: '/materials', icon: <BookIcon /> },
  { 
    label: 'Admin', 
    path: '/admin', 
    icon: <AdminIcon />, 
    roles: ['admin'] 
  },
  { 
    label: 'Profile', 
    path: '/profile', 
    icon: <AccountIcon /> 
  },
];

const Navigation = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userRole, setUserRole] = useState<string>('user');
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const pathname = usePathname();

  // ユーザーロールの取得（実際のアプリケーションではAuthコンテキストから取得）
  useEffect(() => {
    // TODO: 実際のユーザーロールを取得する処理を実装
    const fetchUserRole = async () => {
      // const role = await getUserRole();
      // setUserRole(role);
    };
    fetchUserRole();
  }, []);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const isActiveLink = (path: string) => {
    return pathname === path;
  };

  // フィルタリングされたナビゲーション項目
  const filteredNavItems = navItems.filter(
    item => !item.roles || item.roles.includes(userRole)
  );

  const renderNavItems = () => (
    <List>
      {filteredNavItems.map((item) => (
        <Link
          href={item.path}
          key={item.path}
          style={{ textDecoration: 'none', color: 'inherit' }}
        >
          <ListItem
            button
            selected={isActiveLink(item.path)}
            sx={{
              '&.Mui-selected': {
                backgroundColor: theme.palette.primary.light,
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItem>
        </Link>
      ))}
    </List>
  );

  return (
    <>
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: 2 }}>
              {renderNavItems()}
            </Box>
          )}
        </Toolbar>
      </AppBar>

      {isMobile && (
        <Drawer
          variant="temporary"
          anchor="left"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // モバイルでのパフォーマンス向上のため
          }}
          sx={{
            '& .MuiDrawer-paper': { 
              width: 240,
              boxSizing: 'border-box' 
            },
          }}
        >
          {renderNavItems()}
        </Drawer>
      )}
    </>
  );
};

export default Navigation;