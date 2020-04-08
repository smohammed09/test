public class Employee {
  String name;
  String dept;

  public String getName() {
      printCurrentMethodName();
      return name;
  }

  public void setName(String name) {
      printCurrentMethodName();
      this.name = name;
  }

  public String getDept() {
      printCurrentMethodName();
      return dept;
  }

  public void setDept(String dept) {
      printCurrentMethodName();
      this.dept = dept;
  }

  private void printCurrentMethodName() {
      //using java 9 stack walker to get current method name
      String methodName = StackWalker.getInstance()
                                     .walk(s -> s.skip(1).findFirst())
                                     .get()
                                     .getMethodName();
      System.out.println("method called: " + methodName);
  }
}