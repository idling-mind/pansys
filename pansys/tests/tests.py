import unittest
from pansys import Ansys
import os

class TestStartup(unittest.TestCase):
     
    def test_wrong_command(self):
        """Checking if a wrong command will raise an OSError"""
        with self.assertRaises(OSError):
            a = Ansys(startcommand="ansys1212121")
            a = Ansys(startcommand="ansys150 -p abcd")
            a = Ansys(startcommand="ls")

    def test_notnone_default(self):
        """Check if ansys was able to start normally"""
        a = Ansys()
        self.assertNotEqual(a, None)

    def test_notnone_custom(self):
        """Check if a custom version of ansys was able to start"""
        a = Ansys(startcommand="ansys130")
        self.assertNotEqual(a, None)

    def test_startfolder_nonexisting(self):
        """Check if an OSError is raised when a nonexistant folder is input as
        working directory"""
        sf = "NoneExisting"
        with self.assertRaises(OSError):
            a = Ansys(startfolder=sf)
    
    def test_startfolder_none(self):
        """Check if working directory is created if nothing is given as input"""
        a = Ansys()
        self.assertEqual(os.path.isdir(a.wd), True)

    def test_cleanup(self):
        """Test if cleanup flag is deleting the folder and vice versa"""
        a = Ansys(cleanup=True)
        wd = a.wd
        a = None
        self.assertEqual(os.path.isdir(wd), False)
        a = Ansys(cleanup=False)
        wd = a.wd
        a = None
        self.assertEqual(os.path.isdir(wd), True)

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)


class TestSendCommand(unittest.TestCase):

    def test_version(self):
        """Checking version of ansys"""
        a = Ansys()
        self.assertEqual(a.version, 15)

    def test_set_get_ansvar(self):
        """Test if send command is working by setting an ansys variable and
        retrieving it. """
        a = Ansys()
        a.send("/prep7")
        a.send("myvar=29323")
        a.send("/com %%myvar%")
        self.assertTrue("29323" in a.output)

    def test_create_nodes(self):
        """Check if everything is working in general"""
        a = createWheelModel(10)

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)


class TestGet(unittest.TestCase):

    def test_create_nodes(self):
        """Test if get function is able to extract nodal coordinates"""
        a = createWheelModel(10)
        g = a.get("node","","count")
        self.assertEqual(g, 11)
        g = a.get("node",1,"LOC", "X")
        self.assertEqual(g, 0)

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)


class TestGetList(unittest.TestCase):

    def test_nlist_elist(self):
        """Check if get_list("nlist") and get_list("elist") are working"""
        a = createWheelModel(10)
        n = a.get_list("nlist")
        self.assertEqual(n.NODE.max(), 11)
        self.assertEqual(n.X.max(), 1)
        e = a.get_list("elist,,,,1", skiprows=2)
        self.assertEqual(e.ELEM.max(), 10)

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)


class TestPlot(unittest.TestCase):
    def test_plot(self):
        """Check if a plot is getting created or not"""
        a = createWheelModel(10)
        p = a.plot("eplot")
        self.assertTrue(os.path.isfile(p))

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)

class TestQueue(unittest.TestCase):
    def test_run_queue(self):
        """Check if queuing works"""
        a = Ansys(cleanup=True)
        a.send("""
            /prep7
            et,,188
            n,,
            """)
        nspokes=10
        for i in range(nspokes):
            a.queue(f'n,,1,{i/360*nspokes}')
            a.queue(f'e,1,{i+2}')
        a.run_queue()
        g = a.get("node","","count")
        self.assertEqual(g, 11)
        g = a.get("node",1,"LOC", "X")
        self.assertEqual(g, 0)

    def tearDown(self):
        import shutil
        import glob
        for path in glob.glob("pansys_*"):
            shutil.rmtree(path, ignore_errors=True)


def createWheelModel(nspokes):
    a = Ansys(cleanup=True)
    a.send("""
    /prep7
    et,,188
    n,,
    """)
    for i in range(nspokes):
        a.send("n,,1,{}".format(i/360*nspokes))
        a.send("e,1,{}".format(i+2))
    return a

if __name__ == "__main__":
    unittest.main()
