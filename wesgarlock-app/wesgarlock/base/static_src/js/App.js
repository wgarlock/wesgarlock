import React, { Fragment, Suspense } from 'react'
import { MuiThemeProvider, CssBaseline } from '@material-ui/core'
import theme from './theme'
import GlobalStyles from './GlobalStyles'
import Pace from './components/Pace'
import Home from './views/home/Home'

function App () {
  return (
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalStyles />
        <Pace color={theme.palette.primary.light} />
        <Suspense fallback={<Fragment />}>
            <Home />
        </Suspense>
      </MuiThemeProvider>
  )
}

export default App
