/* global  context csrf_input */
import React, { Fragment } from 'react'
import Main from '../../../../base/static_src/js/views/Main'
import PropTypes from 'prop-types'
import { Box, TextField, withStyles, withWidth, Button } from '@material-ui/core'
import classNames from 'classnames'
import parse from 'html-react-parser'

const styles = (theme) => ({
  extraLargeButtonLabel: {
    fontSize: theme.typography.body1.fontSize,
    [theme.breakpoints.up('sm')]: {
      fontSize: theme.typography.h6.fontSize
    }
  },
  extraLargeButton: {
    paddingTop: theme.spacing(1.5),
    paddingBottom: theme.spacing(1.5),
    [theme.breakpoints.up('xs')]: {
      paddingTop: theme.spacing(1),
      paddingBottom: theme.spacing(1)
    },
    [theme.breakpoints.up('lg')]: {
      paddingTop: theme.spacing(2),
      paddingBottom: theme.spacing(2)
    }
  },
  card: {
    boxShadow: theme.shadows[4],
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    [theme.breakpoints.up('xs')]: {
      paddingTop: theme.spacing(3),
      paddingBottom: theme.spacing(3)
    },
    [theme.breakpoints.up('sm')]: {
      paddingTop: theme.spacing(5),
      paddingBottom: theme.spacing(5),
      paddingLeft: theme.spacing(4),
      paddingRight: theme.spacing(4)
    },
    [theme.breakpoints.up('md')]: {
      paddingTop: theme.spacing(5.5),
      paddingBottom: theme.spacing(5.5),
      paddingLeft: theme.spacing(5),
      paddingRight: theme.spacing(5)
    },
    [theme.breakpoints.up('lg')]: {
      paddingTop: theme.spacing(6),
      paddingBottom: theme.spacing(6),
      paddingLeft: theme.spacing(6),
      paddingRight: theme.spacing(6)
    },
    [theme.breakpoints.down('lg')]: {
      width: 'auto'
    }
  },
  wrapper: {
    position: 'relative',
    paddingBottom: theme.spacing(2)
  },
  image: {
    maxWidth: '100%',
    verticalAlign: 'middle',
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[4]
  },
  container: {
    marginTop: theme.spacing(6),
    marginBottom: theme.spacing(12),
    [theme.breakpoints.down('md')]: {
      marginBottom: theme.spacing(9)
    },
    [theme.breakpoints.down('sm')]: {
      marginBottom: theme.spacing(6)
    },
    [theme.breakpoints.down('sm')]: {
      marginBottom: theme.spacing(3)
    }
  },
  containerFix: {
    [theme.breakpoints.up('md')]: {
      maxWidth: 'none !important'
    }
  },
  waveBorder: {
    paddingTop: theme.spacing(4)
  }
})

function Auth (props) {
  const { classes } = props
  return (
    <Main>
      <Fragment>
        <Box>
          <div className={classNames('lg-p-top', classes.wrapper)}>
            <div className={classNames('container-fluid', classes.container)}>
              <form method="POST" action={context.front_urls.password_reset_confirm}>
              {parse(csrf_input)}
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  label="New Password"
                  autoFocus
                  autoComplete="off"
                  type="password"
                  name="new_password1"
                />
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  label="Repeat New Password"
                  autoFocus
                  autoComplete="off"
                  type="password"
                  name="new_password2"
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="secondary"
                  size="large"
                >
                  Submit
                </Button>
              </form>
            </div>
          </div>
        </Box>
      </Fragment>
    </Main>
  )
}

Auth.propTypes = {
  classes: PropTypes.object,
  width: PropTypes.string,
  theme: PropTypes.object
}

export default withWidth()(
  withStyles(styles, { withTheme: true })(Auth)
)
