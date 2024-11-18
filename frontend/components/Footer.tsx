'use client';

import React from 'react';
import Link from 'next/link';
import { Box, Container, Grid, Typography, IconButton, useTheme, useMediaQuery } from '@mui/material';
import { styled } from '@mui/material/styles';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

// スタイル付きコンポーネントの定義
const FooterWrapper = styled('footer')(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(6, 0),
  marginTop: 'auto',
}));

const FooterLink = styled(Link)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  textDecoration: 'none',
  '&:hover': {
    textDecoration: 'underline',
  },
}));

const Footer = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const footerSections = {
    company: {
      title: 'Company',
      links: [
        { text: 'About Us', href: '/about' },
        { text: 'Contact', href: '/contact' },
        { text: 'Careers', href: '/careers' },
      ],
    },
    services: {
      title: 'Services',
      links: [
        { text: 'Online Lessons', href: '/lessons' },
        { text: 'Study Materials', href: '/materials' },
        { text: 'Pricing', href: '/pricing' },
      ],
    },
    legal: {
      title: 'Legal',
      links: [
        { text: 'Terms of Service', href: '/terms' },
        { text: 'Privacy Policy', href: '/privacy' },
        { text: 'Cookie Policy', href: '/cookies' },
      ],
    },
  };

  const socialLinks = [
    { icon: <FacebookIcon />, href: 'https://facebook.com/speakpro' },
    { icon: <TwitterIcon />, href: 'https://twitter.com/speakpro' },
    { icon: <InstagramIcon />, href: 'https://instagram.com/speakpro' },
    { icon: <LinkedInIcon />, href: 'https://linkedin.com/company/speakpro' },
  ];

  return (
    <FooterWrapper>
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          {/* フッターセクション */}
          {Object.entries(footerSections).map(([key, section]) => (
            <Grid item xs={12} sm={4} key={key}>
              <Typography variant="h6" gutterBottom>
                {section.title}
              </Typography>
              <Box component="nav" aria-label={`${section.title} navigation`}>
                {section.links.map((link) => (
                  <Box key={link.href} mb={1}>
                    <FooterLink href={link.href}>
                      <Typography variant="body2">{link.text}</Typography>
                    </FooterLink>
                  </Box>
                ))}
              </Box>
            </Grid>
          ))}

          {/* ソーシャルメディアリンク */}
          <Grid item xs={12}>
            <Box
              display="flex"
              justifyContent={isMobile ? 'center' : 'flex-start'}
              gap={2}
              mt={2}
            >
              {socialLinks.map((link) => (
                <IconButton
                  key={link.href}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Visit our ${link.href.split('.com/')[1]} page`}
                  sx={{ color: 'primary.contrastText' }}
                >
                  {link.icon}
                </IconButton>
              ))}
            </Box>
          </Grid>

          {/* コピーライト */}
          <Grid item xs={12}>
            <Typography
              variant="body2"
              align="center"
              sx={{ mt: 2 }}
            >
              © {new Date().getFullYear()} SpeakPro. All rights reserved.
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </FooterWrapper>
  );
};

export default Footer;